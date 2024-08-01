from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, IntegerType, StringType, StructType, TimestampType, LongType
from pyspark.sql.functions import regexp_extract, col

if __name__ == '__main__':
    spark = SparkSession.builder \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
        .config("spark.jars.packages",
                ###########################################################
                # s3 를 read 하기 위한 필수 jars
                # java.lang.ClassNotFoundException: Class org.apache.hadoop.fs.s3a.S3AFileSystem not found
                ###########################################################
                "org.apache.hadoop:hadoop-aws:3.3.4,"
                ) \
        .appName("AccessLog 1st Parsing") \
        .getOrCreate()
    
    s3_path = "s3a://ken-datalake/source/access/2024/08/01/04/B3Yw509e.json"

    # S3에서 JSON 파일 읽기
    # rdd = spark.sparkContext.textFile(s3_path)
    # # df_zipped = df_zipped = spark \
    # # .read \
    # # .load(s3_path)
    # df = spark.read.json(rdd)
    # df.show()
    # df = spark.read.option("compression", "gzip").json(s3_path)
    # df.show()

    df = spark.read.json(s3_path)
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
    df_final = df_extracted.select("timestamp", "ip", "port", "method", "url", "customer_id", "product_id", "order_id", "status")

    # 결과 출력
    df_final.show(truncate=False)

    # SparkSession 종료
    spark.stop()