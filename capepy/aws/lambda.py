import json


class Record(object):
    """An object for general records in AWS Lambda handlers.

    Attributes:
        body: The body of the record parsed as JSON
    """

    def __init__(self, record):
        """Constructor for instantiating a new Lambda Record

        Args:
            record (object): A record from an AWS Lambda handler event
        """
        self.body = json.loads(record["body"])


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
        self.name = self.body["pipeline_name"]
        self.version = self.body["pipeline_version"]
        self.parameters = self.body["parameters"]


class BucketRecord(Record):
    """An object for S3 bucket related records passed into AWS Lambda handlers.

    Attributes:
        name: The name of the bucket
        key: The key into the bucket if relevant
    """

    def __init__(self, record):
        """Constructor for instantiating a new record of S3 bucket information

        Args:
            record (object): An S3 bucket related record from an AWS Lambda handler event
        """
        super().__init__(record)
        self.name = self.body["bucket_name"]
        self.key = self.body["key"] if "key" in self.body else None
