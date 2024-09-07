from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os
from datetime import datetime, timedelta

if __name__ == '__main__':
    
    min_last_update_time = "2023-01-01 00:00:00"
    # max_last_update_time = "2024-09-06 23:59:59"
    max_last_update_time = "2024-09-05 23:59:59"

    # java.lang.IllegalArgumentException: Too large frame: 5785721462337832960
    # .config("spark.driver.host", "localhost") 추가
    spark_builder = SparkSession.builder \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
        .config("spark.driver.host", "localhost") \
        .config("spark.jars.packages",
                "org.postgresql:postgresql:42.2.23,"
                "org.apache.hadoop:hadoop-aws:3.3.4,"
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
    db_host = "webdb_dev_rw.gshs.co.kr"
    db_port = "5432"
    db_database = "dwebdb"
    url = f"jdbc:postgresql://{db_host}:{db_port}/{db_database}"
    user = "i_chiho"
    password = "gsshop_776"
    table = "smtc_inf.prd_prd_m"
    partitionColumn = "mod_dtm"
    numPartitions = 6
    lowerBound = datetime.strptime(min_last_update_time, "%Y-%m-%d %H:%M:%S")
    upperBound = datetime.strptime(max_last_update_time, "%Y-%m-%d %H:%M:%S")
    fetchsize = 100000

    query = f"""
(
    select *
    from smtc_inf.prd_prd_m
    where mod_dtm >= '{lowerBound}'
    and mod_dtm < '{upperBound}'
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
                .option("fetchsize", fetchsize)
                .load()
    )

    print(f"## {df.count()}")

    # output_path = f"s3a://ken-tmp01/ecommerce/orders7/"
    output_path = f"s3a://s3-clickstream-test-01/tmp/dwebdb/smtc_inf.prd_prd_m/"

    # S3에 Parquet 포맷으로 저장
    df.write \
        .mode("append") \
        .parquet(output_path)


    spark.stop()