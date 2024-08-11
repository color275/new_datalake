from datetime import datetime
import logging
import boto3


def create_dynamodb_table(dynamodb, table_name):
    # 테이블이 없으면 생성
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'table_name',
                    'KeyType': 'HASH'  # 파티션 키
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'table_name',
                    'AttributeType': 'S'  # 'S'는 문자열
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        # 테이블이 생성될 때까지 기다림
        dynamodb.get_waiter('table_exists').wait(TableName=table_name)
        logging.info(f"# DynamoDB Table '{table_name}' has been created.")

    except Exception as e:
        logging.info(f"Error creating DynamoDB Table: {e}")


def get_last_bookmark(dynamodb_table, table_name) -> str :
    response = dynamodb_table.get_item(
        Key={'table_name': table_name}
    )
    if 'Item' in response:
        # last_bookmark_time = datetime.strptime(
        #     response['Item']['last_bookmark_time'], '%Y-%m-%d %H:%M:%S')
        last_bookmark_time = response['Item']['last_bookmark_time']
        return last_bookmark_time
    else:
        logging.info(f"# No Data in {table_name} {dynamodb_table}")
        return None


def set_last_bookmark(dynamodb_table, table_name, last_bookmark_time):
    if isinstance(last_bookmark_time, datetime):
        last_bookmark_time_str = last_bookmark_time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        # 밀리초는 절삭
        last_bookmark_time_str = last_bookmark_time.split('.')[0]

    response = dynamodb_table.update_item(
        Key={'table_name': table_name},
        UpdateExpression="SET last_bookmark_time = :last_bookmark_time, last_update_time = :last_update_time",
        ExpressionAttributeValues={
            ':last_bookmark_time': last_bookmark_time_str,
            ':last_update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        ReturnValues="UPDATED_NEW"
    )
    logging.info(f"Update succeeded: {response}")
