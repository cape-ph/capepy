import os

from botocore.exceptions import ClientError

from capepy.aws.meta import Boto3Object
from capepy.aws.utils import decode_error


class Table(Boto3Object):
    """An object for working with specific DynamoDB Table structures in the CAPE system.

    Attributes:
        name: the name of the table
        table: the table object retrieved with the boto3 dybamodb resource
    """

    def __init__(self, table_name):
        """Constructor for instantiating the DynamoDB table object. Assumes DDB_REGION is set in the environment.

        Args:
            table_name: The name of the table to retrieve from DynamoDB.
        """
        super().__init__()
        ddb = self.get_resource("dybamodb", region_name=os.getenv("DDB_REGION"))
        self.name = table_name

        try:
            self.table = ddb.Table(table_name)
            self.table.load()
        except ClientError as err:
            code, message = decode_error(err)

            if code == "ResourceNotFoundException":
                msg = (
                    f"CAPE DAP registry DynamoDB table ({table_name}) could not"
                    f"be found: {code} {message}",
                )
            else:
                msg = (
                    f"Error trying to access CAPE data analysis pipeline registry "
                    f"DynamoDB table ({table_name}): {code} {message}",
                )

            self.logger.error(msg)
            raise err

    def get_item(self, key):
        """Retrieve an item from the loaded table.

        Args:
            key: The key of the entry to retrieve from the table.

        Returns:
            The item value from the DyamoDB table.
        """
        ret = None
        try:
            ret = self.table.get_item(Key=key)["Item"]

        except ClientError as err:
            code, message = decode_error(err)

            self.logger.error(
                f"Couldn't get DynamoDB entry for key '{key}' in table {self.name}. "
                f"{code} {message}"
            )

        return ret


class PipelineTable(Table):
    """A DynamoDB table with specific structure for organizing analysis pipelines."""

    def __init__(self, table_name):
        """Constructor to fetch and initialize a DynamoDB analysis pipeline table.

        Args:
            table_name: The name of the pipeline table to retrieve from DynamoDB.
        """
        super().__init__(table_name)

    def get_pipeline(self, pipeline_name, pipeline_version):
        """Retrieve a specific pipeline from the table.

        Args:
            pipeline_name: The name of the pipeline.
            pipeline_version: The version of the pipeline.

        Returns:
            The retrieved pipeline item.
        """
        key = {"pipeline_name": pipeline_name}
        if pipeline_version is not None:
            key["version"] = pipeline_version
        return self.get_item(key)


class EtlTable(Table):
    """A DynamoDB table with specific structure for organizing ETL jobs."""

    def __init__(self, table_name):
        """Constructor to fetch and initialize a DynamoDB ETL job table.

        Args:
            table_name: The name of the ETL table to retrieve from DynamoDB.
        """
        super().__init__(table_name)

    def get_etls(self, bucket_name, prefix):
        """Retrieve a specific ETLs from the table.

        Args:
            bucket_name: The name of the s3 bucket to get ETL jobs for.
            prefix: The required prefix to check for ETL jobs.

        Returns:
            The ETL Jobs triggered by the given bucket name and prefix.
        """
        return self.get_item({"bucket_name": bucket_name, "prefix": prefix})