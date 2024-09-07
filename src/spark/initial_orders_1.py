from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, dayofmonth, hour, minute
from datetime import datetime, timedelta
import os

if __name__ == '__main__':

    min_last_update_time = "2024-09-03 22:38:09"
    max_last_update_time = "2024-09-03 23:59:59"

    spark_builder = SparkSession.builder \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
        .config("spark.jars.packages",
                "org.postgresql:postgresql:42.2.23,"
                "org.apache.hadoop:hadoop-aws:3.3.4,"
                ) \
        .appName("PostgreSQL to S3")
    
    spark = spark_builder.getOrCreate()

    db_host = "0.0.0.0"
    # db_host = "database-1.cluster-cgluv9lxvqft.ap-northeast-2.rds.amazonaws.com"
    db_port = "5432"
    db_database = "ecommerce"

    jdbc_url = f"jdbc:postgresql://{db_host}:{db_port}/{db_database}"
    connection_properties = {
        "user": "admin2",
        "password": "Admin1234",
        "driver": "org.postgresql.Driver"
    }

    # 날짜 문자열을 datetime 객체로 변환
    min_time = datetime.strptime(min_last_update_time, "%Y-%m-%d %H:%M:%S")
    max_time = datetime.strptime(max_last_update_time, "%Y-%m-%d %H:%M:%S")

    current_time = min_time

    while current_time < max_time:
        next_time = current_time + timedelta(hours=1)
        
        # next_time이 max_time을 초과하면 max_time으로 설정
        if next_time >= max_time:
            next_time = max_time
        
        # PostgreSQL에서 데이터 읽기
        query = f"""
            SELECT * FROM src.orders
            WHERE last_update_time >= '{current_time.strftime('%Y-%m-%d %H:%M:%S')}'
            AND last_update_time < '{next_time.strftime('%Y-%m-%d %H:%M:%S')}'
        """

        df = spark.read.jdbc(url=jdbc_url, table=f"({query}) AS tmp", properties=connection_properties)

        output_path = f"s3a://ken-tmp01/ecommerce/orders7/"

        # S3에 Parquet 포맷으로 저장
        df.write \
            .mode("append") \
            .parquet(output_path)

        # 다음 시간으로 이동
        current_time = next_time

    spark.stop()