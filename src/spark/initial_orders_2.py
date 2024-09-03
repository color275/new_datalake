from datetime import datetime, timedelta
import logging
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import split, regexp_extract, col, year, month, dayofmonth, hour, to_timestamp, lpad
from pyspark.sql.types import StructField, IntegerType, StringType, StructType, TimestampType, LongType
import boto3
import os
import sys


if __name__ == '__main__':

    catalog_name = "glue_catalog"
    bucket_name = "ken-tmp01"
    database_name = "ecommerce"

    table_name = "orders_test7"

    source_bucket_prefix = f"ecommerce/orders/"
    source_path = f"s3a://{bucket_name}/{source_bucket_prefix}"

    iceberg_bucket_prefix = f"merge/{database_name}/"
    warehouse_path = f"s3a://{bucket_name}/{iceberg_bucket_prefix}"

    ###########################################################################
    # upsert 시 필요
    # org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions
    ###########################################################################

    # 실행 모드 확인
    is_cluster_mode = os.getenv("SPARK_DEPLOY_MODE", "cluster")

    spark_builder = SparkSession.builder \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
        .config(f"spark.sql.catalog.{catalog_name}", "org.apache.iceberg.spark.SparkCatalog") \
        .config(f"spark.sql.catalog.{catalog_name}.catalog-impl", "org.apache.iceberg.aws.glue.GlueCatalog") \
        .config(f"spark.sql.catalog.{catalog_name}.warehouse", f"{warehouse_path}") \
        .config("spark.sql.catalog.glue_catalog.lock-impl", "org.apache.iceberg.aws.dynamodb.DynamoDbLockManager") \
        .config("spark.sql.catalog.glue_catalog.lock.table", "IcebergLockTable") \
        .config("spark.jars.packages",
                ###########################################################
                # iceberg 를 read 하기 위한 필수 jars
                ###########################################################
                "org.apache.iceberg:iceberg-spark-runtime-3.4_2.12:1.5.2,"
                "software.amazon.awssdk:bundle:2.17.230,"
                ###########################################################
                "org.apache.hadoop:hadoop-aws:3.3.4,"
                # "org.apache.iceberg:iceberg-spark-extensions-3.4_2.12:1.5.2,"
                # "software.amazon.awssdk:url-connection-client:2.17.230,"
                # "org.apache.hadoop:hadoop-aws:3.3.4,"
                # "com.amazonaws:aws-java-sdk-bundle:1.11.901,"
                # "com.amazonaws:aws-java-sdk-core:1.12.725,"
                # "com.amazonaws:jmespath-java:1.12.725"
                ) \
        .appName("data merge")

    
    # SparkSession 생성
    spark = spark_builder.getOrCreate()

    df = spark.read.parquet("s3a://ken-tmp01/ecommerce/orders7/")

    df.createOrReplaceTempView("v_cdc_source")
    
    query = f"""
    SELECT
        order_id,
        promo_id,
        order_cnt,
        order_price,
        order_dt,
        last_update_time,
        customer_id,
        product_id
    FROM (
        SELECT
            a.*,
            ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY last_update_time DESC) as row_num
        FROM v_cdc_source a
    ) subquery
    WHERE row_num = 1
    """

    cdc_max_df = spark.sql(query)

    cdc_max_df.createOrReplaceTempView("v_cdc_max")

    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {catalog_name}.{database_name}.{table_name}
        USING iceberg
        AS (
            SELECT  order_id,
                    promo_id,
                    order_cnt,
                    order_price,
                    order_dt,
                    last_update_time,
                    customer_id,
                    product_id
            FROM v_cdc_max
        )
    """)

    # while True :
    #     pass

    spark.stop()