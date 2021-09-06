from aws_cdk import core
from aws_cdk.aws_dynamodb import Attribute, AttributeType, BillingMode, Table
from aws_cdk.aws_lambda import Runtime
from aws_cdk.aws_lambda_event_sources import SqsEventSource
from aws_cdk.aws_lambda_python import PythonFunction
from aws_cdk.aws_sqs import Queue

APP_NAME = "CdkSqsIdempotencyLambda"


class CdkSqsIdempotencyLambdaStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = Table(
            self,
            f"{APP_NAME}IdempotencyStore",
            partition_key=Attribute(name="id", type=AttributeType.STRING),
            time_to_live_attribute="expiration",
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        queue = Queue(self, f"{APP_NAME}Queue")

        lambda_ = PythonFunction(
            self,
            f"{APP_NAME}Lambda",
            entry="lambda_app",
            runtime=Runtime.PYTHON_3_8,
            environment={"IDEMPOTENCY_STORE_TABLE_NAME": table.table_name},
        )

        lambda_.add_event_source(SqsEventSource(queue))

        table.grant_read_write_data(lambda_)
