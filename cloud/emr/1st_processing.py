from datetime import datetime, timedelta
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, IntegerType, StringType, StructType, TimestampType, LongType
from pyspark.sql.functions import regexp_extract, col, hour, dayofmonth, month, year, lpad
import boto3
import logging
import last_batch_time as lbt
import os
from pyspark.sql.functions import to_timestamp

if __name__ == '__main__':
    
    
    is_cluster_mode = os.getenv("SPARK_DEPLOY_MODE", "cluster")

    # 클러스터 모드에서만 적용할 설정 추가
    if is_cluster_mode == "cluster":
        print("## Cluster Mode : True")
    else:
        print("# Cluster Mode : False")

    spark = SparkSession.builder \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
        .config("spark.sql.sources.partitionOverwriteMode", "dynamic") \
        .config("spark.jars.packages",
                ###########################################################
                # s3 를 read 하기 위한 필수 jars
                # java.lang.ClassNotFoundException: Class org.apache.hadoop.fs.s3a.S3AFileSystem not found
                ###########################################################
                "org.apache.hadoop:hadoop-aws:3.3.4,"
                ) \
        .appName("AccessLog 1st Parsing") \
        .getOrCreate()
    
    bucket_name = "ken-datalake"
    table_name = "accesslog"

    dynamodb_table_name = "emr_last_batch_time"
    dynamodb = boto3.client('dynamodb', region_name='ap-northeast-2')
    existing_tables = dynamodb.list_tables()['TableNames']
    if dynamodb_table_name in existing_tables:
        logging.info(f"DynamoDB Table '{dynamodb_table_name}' already exists.")
    else:
        lbt.create_dynamodb_table(dynamodb, dynamodb_table_name)

    dynamodb = boto3.resource('dynamodb', region_name="ap-northeast-2")
    dynamodb_table = dynamodb.Table(dynamodb_table_name)
    
    last_bookmark_time_str = lbt.get_last_bookmark(
        dynamodb_table, f"{table_name}")

    if last_bookmark_time_str:
        last_bookmark_time = datetime.strptime(
            last_bookmark_time_str, '%Y-%m-%d %H:%M:%S')
    else:
        # s3의 파티션된 최소 데이터
        # 처음이라면 현재 시간에서 1시간 전부터 시작
        last_bookmark_time = datetime.now() - timedelta(hours=1)

    
    current_time = datetime.now()

    df = None
    last_bookmark_time_ymdh_str = datetime.strftime(last_bookmark_time, '%Y%m%d%H')
    current_time_ymdh_str = datetime.strftime(current_time, '%Y%m%d%H')
    print(
        f"## last_bookmark_time_ymdh_str({last_bookmark_time_ymdh_str}) <= current_time_ymdh_str({current_time_ymdh_str})")
    while last_bookmark_time_ymdh_str <= current_time_ymdh_str:
        print("# last_bookmark_time : ", last_bookmark_time)
        print("# current_time : ", current_time)
        cdc_partition_time = last_bookmark_time - timedelta(hours=9)
        next_s3_path = f"s3a://{bucket_name}/fluentbit/access/{cdc_partition_time.year}/{cdc_partition_time.month:02}/{cdc_partition_time.day:02}/{cdc_partition_time.hour:02}"
        print("## next_s3_path : ", next_s3_path)

        try:
            if df is None:
                df = spark.read.json(next_s3_path)
                if is_cluster_mode != "cluster":
                    break
            else:
                df = df.union(spark.read.json(next_s3_path))
        except Exception as e:
            print(f"Error reading {next_s3_path}: {e}")

        next_time = last_bookmark_time + timedelta(hours=1)
        last_bookmark_time = next_time

        last_bookmark_time_ymdh_str = datetime.strftime(last_bookmark_time, '%Y%m%d%H')




    # df = spark.read.json(s3_path)
    df.show()


    # "2024-08-01 12:31:20.628" 형식의 로그만 추출
    df_filtered = df.filter(df["log"].rlike(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}"))

    # 필요한 컬럼 추출 및 데이터 정제
    df_extracted = df_filtered.withColumn("timestamp", regexp_extract(col("log"), r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})", 1)) \
        .withColumn("ip", regexp_extract(col("log"), r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", 1)) \
        .withColumn("port", regexp_extract(col("log"), r":(\d+) -", 1)) \
        .withColumn("method", regexp_extract(col("log"), r"\"(GET|POST|PUT|DELETE)", 1)) \
        .withColumn("url", regexp_extract(col("log"), r"\"(?:GET|POST|PUT|DELETE) (\/[^\s]*)", 1)) \
        .withColumn("customer_id", regexp_extract(col("log"), r"login_id=(\d+)", 1)) \
        .withColumn("product_id", regexp_extract(col("log"), r"product_id=(\d+)", 1)) \
        .withColumn("order_id", regexp_extract(col("log"), r"order_id=(\d+)", 1)) \
        .withColumn("status", regexp_extract(col("log"), r"HTTP\/1\.1\" (\d{3})", 1))

    # 필요한 컬럼 선택
    df_sel = df_extracted.select("timestamp", "ip", "port", "method", "url", "customer_id", "product_id", "order_id", "status")

    df_partition = df_sel.withColumn("year", year("timestamp")) \
        .withColumn("month", lpad(month("timestamp"), 2, '0')) \
        .withColumn("day", lpad(dayofmonth("timestamp"), 2, '0')) \
        .withColumn("hour", lpad(hour("timestamp"), 2, '0'))

    # 결과 출력
    df_partition.show(truncate=False)

    df_partition.write \
    .partitionBy("year", "month", "day", "hour") \
    .mode('overwrite') \
    .parquet(f"s3a://{bucket_name}/source/access/")

    latest_time_str = df_partition.agg({"timestamp": "max"}).collect()[0][0]
    if latest_time_str:
        lbt.set_last_bookmark(
            dynamodb_table, f"{table_name}", latest_time_str)

    # SparkSession 종료
    spark.stop()