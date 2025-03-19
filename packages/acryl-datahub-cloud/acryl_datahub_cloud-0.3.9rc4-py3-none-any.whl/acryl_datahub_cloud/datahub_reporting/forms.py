import datetime
import logging
import os
from typing import Dict, List, Optional

import boto3
from pydantic import BaseModel

from acryl_datahub_cloud.datahub_reporting.datahub_dataset import (
    DataHubBasedS3Dataset,
    DatasetMetadata,
    DatasetRegistrationSpec,
    FileStoreBackedDatasetConfig,
)
from acryl_datahub_cloud.datahub_reporting.datahub_form_reporting import (
    DataHubFormReportingData,
)
from acryl_datahub_cloud.datahub_reporting.forms_config import (
    DataHubReportingFormSourceConfig,
    DataHubReportingFormSourceReport,
)
from datahub.emitter.mce_builder import make_dataset_urn
from datahub.ingestion.api.common import PipelineContext
from datahub.ingestion.api.decorators import (
    SupportStatus,
    config_class,
    platform_name,
    support_status,
)
from datahub.ingestion.api.source import Source, SourceReport
from datahub.ingestion.graph.client import DataHubGraph

logger = logging.getLogger(__name__)


class FormAnalyticsConfig(BaseModel):
    enabled: bool
    dataset_urn: Optional[str] = None
    physical_uri_prefix: Optional[str] = None


@platform_name(id="datahub", platform_name="DataHub")
@config_class(DataHubReportingFormSourceConfig)
@support_status(SupportStatus.INCUBATING)
class DataHubReportingFormsSource(Source):
    platform = "datahub"

    def __init__(self, config: DataHubReportingFormSourceConfig, ctx: PipelineContext):
        super().__init__(ctx)
        self.config: DataHubReportingFormSourceConfig = config
        self.report = DataHubReportingFormSourceReport()
        self.opened_files: List[str] = []
        self.s3_client = boto3.client("s3")

    def get_reporting_config(self) -> Optional[FormAnalyticsConfig]:
        query_name = "formAnalyticsConfig"
        field_mappings: Dict[str, str] = {
            "enabled": "enabled",
            "dataset_urn": "datasetUrn",
            "physical_uri_prefix": "physicalUriPrefix",
        }
        query_project_fragment = "\n".join(field_mappings.values())
        form_config_query = f"""
            query {{
                {query_name} {{
                    {query_project_fragment}
                 }}
            }}
            """

        query_result = self.graph.execute_graphql(query=form_config_query)
        if query_result:
            if query_result.get(query_name, {}).get("enabled") is False:
                return FormAnalyticsConfig(
                    enabled=False, dataset_urn=None, physical_uri_prefix=None
                )
            result_map = query_result.get(query_name, {})
            return FormAnalyticsConfig.parse_obj(
                dict(
                    (field, result_map.get(graphql_field))
                    for field, graphql_field in field_mappings.items()
                )
            )
        else:
            return None

    def get_workunits(self):
        self.graph = (
            self.ctx.require_graph("Loading default graph coordinates.")
            if self.config.server is None
            else DataHubGraph(config=self.config.server)
        )
        form_analytics_config = self.get_reporting_config()

        if form_analytics_config and not form_analytics_config.enabled:
            logger.info("Form analytics is not enabled. Skipping reporting.")
            self.report.feature_enabled = False
            return

        form_data = DataHubFormReportingData(self.graph, self.config.forms_include)
        # If form analytics config is not present, use the default reporting bucket prefix
        dataset_uri_prefix = (
            form_analytics_config.physical_uri_prefix
            if form_analytics_config and form_analytics_config.physical_uri_prefix
            else self.config.reporting_bucket_prefix
        )
        if not dataset_uri_prefix:
            raise ValueError(
                "Reporting bucket prefix must be provided. Either configure it on the server side or in the source config."
            )

        registration_spec = DatasetRegistrationSpec()
        dataset_metadata = DatasetMetadata(
            displayName="Forms Reporting Data",
            description="This data was generated by the forms reporting system.",
        )
        dataset_urn = (
            form_analytics_config.dataset_urn
            if form_analytics_config and form_analytics_config.dataset_urn
            else make_dataset_urn(
                self.config.reporting_store_platform, self.config.reporting_dataset_name
            )
        )
        dataset_config = FileStoreBackedDatasetConfig(
            dataset_name="Forms Reporting Dataset",
            store_platform="s3",
            dataset_registration_spec=registration_spec,
            bucket_prefix=dataset_uri_prefix,
            dataset_urn=dataset_urn,
        )
        dataset = DataHubBasedS3Dataset(
            dataset_metadata=dataset_metadata,
            config=dataset_config,
        )
        for row in form_data.get_data(
            lambda x: self.report.increment_assets_scanned(),
            lambda x: self.report.increment_forms_scanned(),
        ):
            dataset.append(row)
        num_workunits = 0
        for mcp in dataset.commit():
            assert mcp.entityUrn, "MCP must have a URN"
            dataset_urn = mcp.entityUrn
            yield mcp.as_workunit()
            num_workunits += 1
        if num_workunits == 0:
            logger.info("No form reporting to be done")
            return
        logger.info(
            f"Reporting file created at {dataset.get_remote_file_uri(dataset_uri_prefix=dataset_uri_prefix, date=datetime.date.today())}"
        )
        logger.info(f"Reporting dataset registered at {dataset_urn}")

        print(f"Dataset {dataset_urn} created successfully")

    def get_report(self) -> SourceReport:
        return self.report

    def close(self) -> None:
        for file in self.opened_files:
            os.remove(file)
        return super().close()
