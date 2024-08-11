from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, dayofmonth, hour
import time
import sys
import os

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Usage: .py <last_update_time>")
        print("ex : 2024-07-01 16:00:00")
        sys.exit(1)
    
    last_update_time = sys.argv[1]

    print(f"# last_update_time : {last_update_time}")

    catalog_name = "glue_catalog"
    bucket_name = "ken-datalake"
    database_name = "ecommerce"

    table_name = "orders_batch"

    iceberg_bucket_prefix = f"source/{database_name}/"
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
                # mysql
                ###########################################################
                "mysql:mysql-connector-java:8.0.28,"
                ###########################################################
                # s3 를 read 하기 위한 필수 jars
                # java.lang.ClassNotFoundException: Class org.apache.hadoop.fs.s3a.S3AFileSystem not found
                ###########################################################
                "org.apache.hadoop:hadoop-aws:3.3.4,"
                ) \
        .appName("MySQL to S3")
    
    # 클러스터 모드에서만 적용할 설정 추가
    if is_cluster_mode == "cluster":
        # local 에서 아래 옵션은 bug가 있다.
        # .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
        print("## Cluster Mode : True")
        spark_builder = spark_builder.config(
            "spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
    else:
        print("# Cluster Mode : False")

    # SparkSession 생성
    spark = spark_builder.getOrCreate()

    # MySQL 연결 정보
    jdbc_url = "jdbc:mysql://data-workshop.cluster-cgluv9lxvqft.ap-northeast-2.rds.amazonaws.com:3306/ecommerce"
    connection_properties = {
        "user": "appuser",
        "password": "appuser",
        "driver": "com.mysql.jdbc.Driver"
    }


    # MySQL에서 데이터 읽기
    query = "SELECT * FROM orders"
    if last_update_time:
        query += f" WHERE last_update_time >= '{last_update_time}'"

    df = spark.read.jdbc(url=jdbc_url, table=f"({query}) AS tmp", properties=connection_properties)

    if df.count() > 0:

        spark.sql(f"CREATE DATABASE IF NOT EXISTS {catalog_name}.{database_name}")

        spark.sql(f"SHOW DATABASES IN {catalog_name}").show()

        spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {catalog_name}.{database_name}.{table_name} (
            order_id INT,
            promo_id STRING,
            order_cnt INT,
            order_price INT,
            order_dt STRING,
            last_update_time TIMESTAMP,
            customer_id INT,
            product_id INT,
            year INT,
            month INT,
            day INT,
            hour INT
        ) USING iceberg
        PARTITIONED BY (year, month, day, hour)
        """)

        # 파티션 컬럼 생성
        df = df.withColumn("year", year(col("last_update_time"))) \
                .withColumn("month", month(col("last_update_time"))) \
                .withColumn("day", dayofmonth(col("last_update_time"))) \
                .withColumn("hour", hour(col("last_update_time")))

        df.createOrReplaceTempView("df")

        spark.sql(f"""MERGE INTO {catalog_name}.{database_name}.{table_name} t
        USING df s ON s.order_id = t.order_id
        WHEN MATCHED THEN UPDATE SET *
        WHEN NOT MATCHED THEN INSERT *
        """)

        spark.stop()