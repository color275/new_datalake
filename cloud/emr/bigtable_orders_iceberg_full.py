from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, IntegerType, StringType, StructType, TimestampType, LongType
from pyspark.sql.functions import hour, dayofmonth, month, year, lpad

if __name__ == '__main__':
    catalog_name = "glue_catalog"
    bucket_name = "ken-datalake"
    database_name = "ecommerce"

    table_name = "big_orders"
    
    source_bucket_prefix = f"exports/database-1-snapshot-1723813358/export-database-1-snapshot-1723813358-1723813604/ecommerce/src.orders/1/part-00000-6a0c8180-667d-4804-bfdb-c66f6712c28e-c000.gz.parquet"
    source_path = f"s3a://ken-tmp01/{source_bucket_prefix}"

    iceberg_bucket_prefix = f"source/{database_name}/"
    warehouse_path = f"s3a://{bucket_name}/{iceberg_bucket_prefix}"

    spark = SparkSession.builder \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
        .config(f"spark.sql.catalog.{catalog_name}", "org.apache.iceberg.spark.SparkCatalog") \
        .config(f"spark.sql.catalog.{catalog_name}.catalog-impl", "org.apache.iceberg.aws.glue.GlueCatalog") \
        .config(f"spark.sql.catalog.{catalog_name}.warehouse", f"{warehouse_path}") \
        .config("spark.default.parallelism", "20") \
        .config("spark.sql.shuffle.partitions", "20") \
        .config("spark.jars.packages",
                ###########################################################
                # iceberg 를 read 하기 위한 필수 jars
                ###########################################################
                "org.apache.iceberg:iceberg-spark-runtime-3.4_2.12:1.5.2,"
                "software.amazon.awssdk:bundle:2.17.230,"
                ###########################################################
                ###########################################################
                # s3 를 read 하기 위한 필수 jars
                # java.lang.ClassNotFoundException: Class org.apache.hadoop.fs.s3a.S3AFileSystem not found
                ###########################################################
                "org.apache.hadoop:hadoop-aws:3.3.4,"
                # "org.apache.iceberg:iceberg-spark-extensions-3.4_2.12:1.5.2,"
                # "software.amazon.awssdk:url-connection-client:2.17.230,"
                # "org.apache.hadoop:hadoop-aws:3.3.4,"
                # "com.amazonaws:aws-java-sdk-bundle:1.11.901,"
                # "com.amazonaws:aws-java-sdk-core:1.12.725,"
                # "com.amazona  ws:jmespath-java:1.12.725"
                ) \
        .appName("Orders Iceberg Full") \
        .getOrCreate()

    df = spark.read \
        .parquet(f'{source_path}/')
    
    df = df.withColumn("year", year("last_update_time")) \
        .withColumn("month", lpad(month("last_update_time"), 2, '0')) \
        .withColumn("day", lpad(dayofmonth("last_update_time"), 2, '0')) \
        .withColumn("hour", lpad(hour("last_update_time"), 2, '0'))

    df.show(10)

    df.createOrReplaceTempView(table_name)

    spark.sql(f"CREATE DATABASE IF NOT EXISTS {catalog_name}.{database_name}")

    spark.sql(f"SHOW DATABASES IN {catalog_name}").show()

    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {catalog_name}.{database_name}.{table_name}
        USING iceberg
        PARTITIONED BY (year, month, day, hour)
        AS (
            SELECT  order_id,
                    order_cnt,
                    order_price,
                    order_dt,
                    last_update_time,
                    customer_id,
                    product_id,
                    year,
                    month,
                    day,
                    hour
            FROM {table_name}
        )
    """)

    spark.stop()
