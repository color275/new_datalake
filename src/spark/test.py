from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os
from datetime import datetime, timedelta

if __name__ == '__main__':
    
    min_last_update_time = "2024-09-03 22:40:00"
    max_last_update_time = "2024-09-03 23:50:00"

    # java.lang.IllegalArgumentException: Too large frame: 5785721462337832960
    # .config("spark.driver.host", "localhost") 추가
    spark_builder = SparkSession.builder \
        .config("spark.driver.host", "localhost") \
        .config("spark.jars.packages",
                "org.postgresql:postgresql:42.2.23,"
                ) \
        .appName("PostgreSQL to S3")
    
    spark = spark_builder.getOrCreate()

    
    # connection_properties = {
    #     "user": "admin2",
    #     "password": "Admin1234",
    #     "driver": "org.postgresql.Driver"
    # }

    # 날짜 문자열을 datetime 객체로 변환
    

    # query = "SELECT abc_id, name FROM tb_abc WHERE abc_id BETWEEN 'abc00001' AND 'abc3000000000'"
    
    # 데이터를 읽어올 때 파티션 수를 설정하여 병렬로 작업 수행
    # df = spark.read.jdbc(
    #     url=jdbc_url, 
    #     table=f"({query}) AS tb_abc", 
    #     properties=connection_properties,
    #     numPartitions=10,  # 파티션 수 설정
    #     column="abc_id",  # 파티셔닝에 사용할 열
    #     lowerBound=1,  # 파티셔닝의 최소 값
    #     upperBound=3000000000  # 파티셔닝의 최대 값
    # )

    driver = "org.postgresql.Driver"
    db_host = "localhost"
    db_port = "5432"
    db_database = "ecommerce"
    url = f"jdbc:postgresql://{db_host}:{db_port}/{db_database}"
    user = "admin2"
    password = "Admin1234"
    table = "src.orders"
    partitionColumn = "last_update_time"
    numPartitions = 4
    lowerBound = datetime.strptime(min_last_update_time, "%Y-%m-%d %H:%M:%S")
    upperBound = datetime.strptime(max_last_update_time, "%Y-%m-%d %H:%M:%S")

    query = f"""
(
    select *
    from src.orders
    where last_update_time >= '{lowerBound}'
    and last_update_time < '{upperBound}'
) as sq
"""

    print(f"{lowerBound}, {upperBound}")

    df = (
            spark.read.format("jdbc")
                .option("driver", driver)
                .option("url", url)
                .option("user", user)
                .option("password", password)
                .option("dbtable", query)
                .option("partitionColumn", partitionColumn)
                .option("numPartitions",numPartitions)
                .option("lowerBound", lowerBound)
                .option("upperBound", upperBound)
                .load()
    )

    df.collect()

    while True :
        pass

    spark.stop()