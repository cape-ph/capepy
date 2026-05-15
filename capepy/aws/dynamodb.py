import os

from boto3.dynamodb.conditions import ConditionExpressionBuilder, Key
from botocore.exceptions import ClientError

from capepy.aws.meta import Boto3Object
from capepy.aws.utils import decode_error


class Table(Boto3Object):
    """An object for working with specific DynamoDB Table structures in the CAPE system.

    Attributes:
        name: the name of the table
        table: the table object retrieved with the boto3 dynamodb resource
    """

    def __init__(self, table_name):
        """Constructor for instantiating the DynamoDB table object. Assumes DDB_REGION is set in the environment.

        Args:
            table_name: The name of the table to retrieve from DynamoDB.
        """
        super().__init__()
        ddb = self.get_resource("dynamodb", region_name=os.getenv("DDB_REGION"))
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
                    f"Error trying to access CAPE DynamoDB table ({table_name}): "
                    f"{code} {message}",
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
            response = self.table.get_item(Key=key)
            ret = response.get("Item")

        except ClientError as err:
            code, message = decode_error(err)

            self.logger.error(
                f"Couldn't get DynamoDB entry for key '{key}' in table {self.name}. "
                f"{code} {message}"
            )

        return ret

    def query_items(self, index_name, key_cond_exp):
        """Retrieve items from the loaded table using a secondary index.

        Args:
            index_name: The name of the index to query.
            key_cond_exp: The key condition expression to use in the query.

        Returns:
            The items value from the DyamoDB table. Any valid query results
            will come back as a list (including an empty list for no match),
            None is returned if there is an error.
        """
        ret = None

        try:
            response = self.table.query(
                IndexName=index_name, KeyConditionExpression=key_cond_exp
            )
            ret = response.get("Items")

        except ClientError as err:
            code, message = decode_error(err)

            # the key condition is not real easy to print in a good way, but we
            # do our best.
            ceb = ConditionExpressionBuilder()
            kce = ceb.build_expression(key_cond_exp, is_key_condition=True)

            kce_str = (
                f"Expression: {kce.condition_expression} "
                f"Expression Attr Names: {kce.attribute_name_placeholders} "
                f"Expression Attr Values: {kce.attribute_value_placeholders} "
            )

            self.logger.error(
                f"Couldn't get DynamoDB entries for in index '{index_name}' "
                f"with key condition expression '{kce_str}' in table {self.name}. "
                f"{code} {message}"
            )

        return ret


class PipelineTable(Table):
    """A DynamoDB table with specific structure for organizing analysis pipelines."""

    # name of the index that we query with name and version
    NAME_VER_GSI = "PipelineNameVerIndex"

    def __init__(self, table_name=None):
        """Constructor to fetch and initialize a DynamoDB analysis pipeline table.

        Args:
            table_name: The name of the pipeline table to retrieve from DynamoDB. Defaults to $DAP_REG_DDB_TABLE
        """
        if table_name is None:
            table_name = os.getenv("DAP_REG_DDB_TABLE")
        super().__init__(table_name)

    def get_pipelines_by_name(self, pipeline_name, pipeline_version=None):
        """Retrieve pipelines from the table matching name and optional version.

        Args:
            pipeline_name: The name of the pipeline.
            pipeline_version: The optional version of the pipeline.

        Returns:
            The retrieved pipeline item(s) in a list (which will be empty in the
            case of no match) or None on error.
        """
        kce = Key("pipeline_name").eq(pipeline_name)

        if pipeline_version is not None:
            kce = kce & Key("version").eq(pipeline_version)

        return self.query_items(self.NAME_VER_GSI, kce)

    def get_pipeline(self, pipeline_id):
        """Retrieve a specific pipeline from the table.

        Args:
            pipeline_id: The id of the pipeline.

        Returns:
            The retrieved pipeline item.
        """
        key = {"pipeline_id": pipeline_id}
        return self.get_item(key)


class WorkflowMetaTable(Table):
    """A DynamoDB table with specific structure for airflow workflow metadata.

    This table contains a mapping of workflow DAG IDs to Pipeline IDs for
    pipelines used in the workflow.
    """

    def __init__(self, table_name=None):
        """Constructor to fetch and initialize a DynamoDB analysis pipeline table.

        Args:
            table_name: The name of the pipeline table to retrieve from DynamoDB. Defaults to $DAP_REG_DDB_TABLE
        """
        if table_name is None:
            table_name = os.getenv("WORKFLOW_REG_DDB_TABLE")
        super().__init__(table_name)

    def get_workflow_by_id(self, dag_id):
        """Retrieve a specific workflow entry from the table.

        Args:
            dag_id: The id of the workflow.

        Returns:
            The retrieved workflow item.
        """
        key = {"dag_id": dag_id}
        return self.get_item(key)


class EtlTable(Table):
    """A DynamoDB table with specific structure for organizing ETL jobs."""

    def __init__(self, table_name=None):
        """Constructor to fetch and initialize a DynamoDB ETL job table.

        Args:
            table_name: The name of the ETL table to retrieve from DynamoDB. Defaults to $ETL_ATTRS_DDB_TABLE
        """
        if table_name is None:
            table_name = os.getenv("ETL_ATTRS_DDB_TABLE")
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


class CrawlerTable(Table):
    """A DynamoDB table with specific structure for organizing Glue Crawlers."""

    def __init__(self, table_name=None):
        """Constructor to fetch and initialize a DynamoDB glue crawler table.

        Args:
            table_name: The name of the crawler table to retrieve from DynamoDB. Defaults to $CRAWLER_ATTRS_DDB_TABLE
        """
        if table_name is None:
            table_name = os.getenv("CRAWLER_ATTRS_DDB_TABLE")
        super().__init__(table_name)

    def get_crawler(self, bucket_name):
        """Retrieve a specific crawler from the table.

        Args:
            bucket_name: The name of the bucket.

        Returns:
            The retrieved crawler item.
        """
        return self.get_item({"bucket_name": bucket_name})


class UserTable(Table):
    """A DynamoDB table with specific structure for managing CAPE users."""

    def __init__(self, table_name=None):
        """Constructor to fetch and initialize a DynamoDB user table.

        Args:
            table_name: The name of the user table to retrieve from DynamoDB. Defaults to $USER_ATTRS_DDB_TABLE
        """
        if table_name is None:
            table_name = os.getenv("USER_ATTRS_DDB_TABLE")
        super().__init__(table_name)

    def get_user(self, user_id):
        """Retrieve a specific user from the table.

        Args:
            user_id: The id of the user.

        Returns:
            The retrieved user attributes.
        """
        return self.get_item({"user_id": user_id})


class CannedReportTable(Table):
    """A DynamoDB table with specific structure for managing CAPE reports."""

    def __init__(self, table_name=None):
        """Constructor to fetch and initialize a DynamoDB user table.

        Args:
            table_name: The name of the canned report table to retrieve from
                        DynamoDB. Defaults to $CANNED_REPORT_DDB_TABLE
        """
        if table_name is None:
            table_name = os.getenv("CANNED_REPORT_DDB_TABLE")
        super().__init__(table_name)

    def get_report(self, report_id):
        """Retrieve a specific report entry from the table.

        Args:
            report_id: The id of the report.

        Returns:
            The retrieved report item.
        """
        return self.get_item({"report_id": report_id})
