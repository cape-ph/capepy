import json
from urllib.parse import unquote_plus


class Record(object):
    """An object for general records in AWS Lambda handlers.

    Attributes:
        raw: The raw record
    """

    def __init__(self, record):
        """Constructor for instantiating a new Lambda Record

        Args:
            record (object): A record from an AWS Lambda handler event
        """
        self.raw = record


class BucketNotificationRecord(Record):
    """An object for S3 bucket notification related records passed into AWS Lambda handlers.

    Attributes:
        bucket: The name of the bucket
        key: The key into the bucket if relevant
    """

    def __init__(self, record):
        """Constructor for instantiating a new record of S3 bucket information

        Args:
            record (object): An S3 bucket related record from an AWS Lambda handler event
        """
        super().__init__(record)
        self.bucket = self.raw["s3"]["bucket"]["name"]
        self.key = unquote_plus(
            self.raw["s3"]["object"]["key"], encoding="utf-8"
        )


class ETLRecord(Record):
    """An object for ETL related records passed into AWS Lambda handlers.

    Attributes:
        job: The name of the ETL Job
        bucket: The name of the bucket
        key: The key into the bucket if relevant
    """

    def __init__(self, record):
        """Constructor for instantiating a new record of S3 bucket information

        Args:
            record (object): An S3 bucket related record from an AWS Lambda handler event
        """
        super().__init__(record)
        body = json.loads(self.raw["body"])
        self.job = body["etl_job"]
        self.bucket = body["bucket"]
        self.key = body["key"]


class PipelineRecord(Record):
    """An object for pipeline records passed into AWS Lambda handlers.

    Attributes:
        name: The name of the analysis pipeline
        version: The version of the analysis pipeline
        parameters: A dictionary of parameters to pass to the analysis pipeline
    """

    def __init__(self, record):
        """Constructor for instantiating a new record of an analysis pipeline

        Args:
            record (object): An analysis pipeline related record from an AWS Lambda handler event
        """
        super().__init__(record)
        body = json.loads(self.raw["body"])
        self.name = body["pipeline_name"]
        self.version = body["pipeline_version"]
        self.parameters = body["parameters"]
