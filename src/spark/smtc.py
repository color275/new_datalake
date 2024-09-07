from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os
from datetime import datetime, timedelta

if __name__ == '__main__':
    
    min_last_update_time = "2024-01-04 00:00:00"
    max_last_update_time = "2024-01-05 23:59:59"

    # java.lang.IllegalArgumentException: Too large frame: 5785721462337832960
    # .config("spark.driver.host", "localhost") 추가
    spark_builder = SparkSession.builder \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
        .config("spark.driver.host", "localhost") \
        .config("spark.jars.packages", 
                "com.oracle.database.jdbc:ojdbc6:11.2.0.4,"
                "org.apache.hadoop:hadoop-aws:3.3.4") \
        .appName("Oracle to S3")
    
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
    driver = "oracle.jdbc.OracleDriver"
    db_host = "smtc_dev_rw.gshs.co.kr"
    db_port = "1630"
    db_database = "DEVSMTC"
    # jdbc:oracle:thin:@your_oracle_host:1521:your_service_name
    url = f"jdbc:oracle:thin:@{db_host}:{db_port}:{db_database}"
    user = "i_chiho"
    password = "gsshop_776"
    table = "smtc_own.prd_prd_m"
    partitionColumn = "mod_dtm"
    numPartitions = 6
    lowerBound = f"to_date('{min_last_update_time}','YYYY-MM-DD HH24:MI:SS')"
    upperBound = f"to_date('{max_last_update_time}','YYYY-MM-DD HH24:MI:SS')"
    fetchsize = 10000

    query = f"""
(
    select *
    from smtc_own.prd_prd_m
    where mod_dtm >= {lowerBound}
    and mod_dtm < {upperBound}
) sq
"""

    df = (
            spark.read.format("jdbc")
                .option("driver", driver)
                .option("url", url)
                .option("user", user)
                .option("password", password)
                .option("dbtable", query)
                .option("partitionColumn", partitionColumn)
                .option("numPartitions",numPartitions)
                .option("lowerBound", min_last_update_time)
                .option("upperBound", max_last_update_time)
                .option("dateFormat", "YYYY-MM-DD HH24:MI:SS" )
                .option("oracle.jdbc.mapDateToTimestamp", "false")
                .option("sessionInitStatement", "ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'")
                .option("fetchsize", fetchsize)
                .load()
    )

    print(f"## {df.count()}")

    # output_path = f"s3a://ken-tmp01/ecommerce/orders7/"
    output_path = f"s3a://s3-clickstream-test-01/tmp/dsmtcdb/smtc_own.prd_prd_m/"

    # S3에 Parquet 포맷으로 저장
    df.write \
        .mode("append") \
        .parquet(output_path)


    spark.stop()