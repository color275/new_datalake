from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, IntegerType, StringType, StructType, TimestampType, LongType
from pyspark.sql.functions import hour, dayofmonth, month, year, lpad

if __name__ == '__main__':
    catalog_name = "glue_catalog"
    bucket_name = "ken-datalake"
    database_name = "ecommerce"

    table_name = "customer"

    source_bucket_prefix = f"dms/{database_name}/{table_name}"
    source_path = f"s3a://{bucket_name}/{source_bucket_prefix}"

    iceberg_bucket_prefix = f"source/{database_name}/"
    warehouse_path = f"s3a://{bucket_name}/{iceberg_bucket_prefix}"

    spark = SparkSession.builder \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
        .config(f"spark.sql.catalog.{catalog_name}", "org.apache.iceberg.spark.SparkCatalog") \
        .config(f"spark.sql.catalog.{catalog_name}.catalog-impl", "org.apache.iceberg.aws.glue.GlueCatalog") \
        .config(f"spark.sql.catalog.{catalog_name}.warehouse", f"{warehouse_path}") \
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
        .appName("customer Iceberg Full") \
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
            SELECT  customer_id,
                    password,
                    last_login,
                    is_superuser,
                    username,
                    first_name,
                    last_name,
                    email,
                    is_staff,
                    is_active,
                    date_joined,
                    phone_number,
                    age,
                    gender,
                    address,
                    last_update_time,
                    name,
                    year,
                    month,
                    day,
                    hour
            FROM {table_name} 
        )
    """)

    spark.stop()
