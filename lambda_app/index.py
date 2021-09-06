import json
import os

from aws_lambda_powertools.utilities.batch import sqs_batch_processor
from aws_lambda_powertools.utilities.idempotency import (
    DynamoDBPersistenceLayer,
    IdempotencyConfig,
    idempotent_function,
)

persistence_layer = DynamoDBPersistenceLayer(table_name=os.getenv("IDEMPOTENCY_STORE_TABLE_NAME"))

config = IdempotencyConfig(event_key_jmespath="body")


@idempotent_function(data_keyword_argument="record", config=config, persistence_store=persistence_layer)
def record_handler(record):
    print(f"メッセージ毎の処理するよ！{json.dumps(record['body'])}")
    return record


@sqs_batch_processor(record_handler=record_handler)
def handler(event, context):
    print(f"ハンドラーだよ!{json.dumps([x['body'] for x in event['Records']])}")
    return {"statusCode": 200}
