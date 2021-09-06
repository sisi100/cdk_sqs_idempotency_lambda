import os

from aws_cdk import core

from cdk_sqs_idempotency_lambda.cdk_sqs_idempotency_lambda_stack import CdkSqsIdempotencyLambdaStack

app = core.App()
CdkSqsIdempotencyLambdaStack(app, "CdkSqsIdempotencyLambdaStack")

app.synth()
