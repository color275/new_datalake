from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os
from datetime import datetime, timedelta

if __name__ == '__main__':
    
    lowerBound = 1
    upperBound = 50
    numPartitions = 50

    # java.lang.IllegalArgumentException: Too large frame: 5785721462337832960
    # .config("spark.driver.host", "localhost")
    # sudo wget https://repo1.maven.org/maven2/com/oracle/database/jdbc/ojdbc6/11.2.0.4/ojdbc6-11.2.0.4.jar
    spark_builder = SparkSession.builder \
        .config("spark.hadoop.fs.s3.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
        .config("spark.sql.parquet.int96RebaseModeInWrite", "LEGACY") \
        .config("spark.jars.packages", 
                "com.oracle.database.jdbc:ojdbc6:11.2.0.4,"
                "org.apache.hadoop:hadoop-aws:3.3.4") \
        .appName("Oracle to S3")
    
    spark = spark_builder.getOrCreate()
  
    
    driver = "oracle.jdbc.OracleDriver"
    db_host = "smtc_dev_rw.gshs.co.kr"
    db_port = "1630"
    db_database = "DEVSMTC"
    url = f"jdbc:oracle:thin:@{db_host}:{db_port}:{db_database}"
    user = "i_chiho"
    password = "gsshop_776"
    table = "smtc_own.ord_item_d"
    partitionColumn = "num_partition"
    fetchsize = 100000

    # num-executors 3
    # executor-cores 3
    # executor-memory 8G

    query = f"""
(
    SELECT  *
    FROM
    (
        SELECT /*+ full(a) parallel(a 2) */
        CASE 
            when to_char(mod_dtm, 'YYYYMM') = '202409' THEN 1
            when to_char(mod_dtm, 'YYYYMM') = '202408' THEN 1
            when to_char(mod_dtm, 'YYYYMM') = '202407' THEN 1
            when to_char(mod_dtm, 'YYYYMM') = '202405' THEN 1
            when to_char(mod_dtm, 'YYYYMM') = '202404' THEN 2
            when to_char(mod_dtm, 'YYYYMM') = '202403' THEN 3
            when to_char(mod_dtm, 'YYYYMM') = '202402' THEN 4
            when to_char(mod_dtm, 'YYYYMM') = '202401' THEN 5
            when to_char(mod_dtm, 'YYYYMM') = '202312' THEN 6
            when to_char(mod_dtm, 'YYYYMM') = '202311' THEN 7
            when to_char(mod_dtm, 'YYYYMM') = '202310' THEN 8
            when to_char(mod_dtm, 'YYYYMM') = '202309' THEN 9
            when to_char(mod_dtm, 'YYYYMM') = '202308' THEN 10
            when to_char(mod_dtm, 'YYYYMM') = '202307' THEN 11
            when to_char(mod_dtm, 'YYYYMM') = '202306' THEN 12
            when to_char(mod_dtm, 'YYYYMM') = '202305' THEN 13
            when to_char(mod_dtm, 'YYYYMM') = '202304' THEN 14
            when to_char(mod_dtm, 'YYYYMM') = '202303' THEN 15
            when to_char(mod_dtm, 'YYYYMM') = '202302' THEN 16
            when to_char(mod_dtm, 'YYYYMM') = '202301' THEN 17
            when to_char(mod_dtm, 'YYYYMM') = '202212' THEN 18
            when to_char(mod_dtm, 'YYYYMM') = '202211' THEN 19
            when to_char(mod_dtm, 'YYYYMM') = '202210' THEN 20
            when to_char(mod_dtm, 'YYYYMM') = '202209' THEN 21
            when to_char(mod_dtm, 'YYYYMM') = '202208' THEN 22
            when to_char(mod_dtm, 'YYYYMM') = '202207' THEN 23
            when to_char(mod_dtm, 'YYYYMM') = '202206' THEN 24
            when to_char(mod_dtm, 'YYYYMM') = '202205' THEN 25
            when to_char(mod_dtm, 'YYYYMM') = '202204' THEN 26
            when to_char(mod_dtm, 'YYYYMM') = '202203' THEN 27
            when to_char(mod_dtm, 'YYYYMM') = '202202' THEN 28
            when to_char(mod_dtm, 'YYYYMM') = '202201' THEN 29
            when to_char(mod_dtm, 'YYYYMM') = '202112' THEN 30
            when to_char(mod_dtm, 'YYYYMM') = '202111' THEN 31
            when to_char(mod_dtm, 'YYYYMM') = '202110' THEN 32
            when to_char(mod_dtm, 'YYYYMM') = '202109' THEN 33
            when to_char(mod_dtm, 'YYYYMM') = '202108' THEN 34
            when to_char(mod_dtm, 'YYYYMM') = '202107' THEN 35
            when to_char(mod_dtm, 'YYYYMM') = '202106' THEN 36
            when to_char(mod_dtm, 'YYYYMM') = '202105' THEN 37
            when to_char(mod_dtm, 'YYYYMM') = '202104' THEN 38
            when to_char(mod_dtm, 'YYYYMM') = '202103' THEN 39
            when to_char(mod_dtm, 'YYYYMM') = '202102' THEN 40
            when to_char(mod_dtm, 'YYYYMM') = '202101' THEN 41
            when to_char(mod_dtm, 'YYYYMM') = '202012' THEN 42
            when to_char(mod_dtm, 'YYYYMM') = '202011' THEN 43
            when to_char(mod_dtm, 'YYYYMM') = '202010' THEN 44
            when to_char(mod_dtm, 'YYYYMM') = '202009' THEN 45
            when to_char(mod_dtm, 'YYYYMM') = '202008' THEN 45
            when to_char(mod_dtm, 'YYYYMM') = '202007' THEN 45
            when to_char(mod_dtm, 'YYYYMM') = '202006' THEN 45
            when to_char(mod_dtm, 'YYYYMM') = '202005' THEN 45
            when to_char(mod_dtm, 'YYYYMM') = '202004' THEN 45
            when to_char(mod_dtm, 'YYYYMM') = '202003' THEN 45
            when to_char(mod_dtm, 'YYYYMM') = '202002' THEN 46
            when to_char(mod_dtm, 'YYYYMM') = '202001' THEN 46
            when to_char(mod_dtm, 'YYYYMM') = '201912' THEN 46
            when to_char(mod_dtm, 'YYYYMM') = '201911' THEN 47
            when to_char(mod_dtm, 'YYYYMM') = '201910' THEN 47
            when to_char(mod_dtm, 'YYYYMM') = '201909' THEN 48
            when to_char(mod_dtm, 'YYYYMM') = '201908' THEN 48
            when to_char(mod_dtm, 'YYYYMM') = '201907' THEN 48
            when to_char(mod_dtm, 'YYYYMM') = '201906' THEN 48
            when to_char(mod_dtm, 'YYYYMM') = '201905' THEN 48
            when to_char(mod_dtm, 'YYYYMM') = '201904' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201903' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201902' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201901' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201812' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201811' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201810' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201809' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201808' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201807' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201806' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201805' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201804' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201803' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201802' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201801' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201712' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201711' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201710' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201709' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201708' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201707' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201706' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201705' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201704' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201703' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201702' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201701' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201612' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201611' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201610' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201609' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201608' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201607' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201606' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201605' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201604' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201603' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201602' THEN 49
            when to_char(mod_dtm, 'YYYYMM') = '201601' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201512' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201511' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201510' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201509' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201508' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201507' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201506' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201505' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201504' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201503' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201502' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201501' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201412' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201411' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201410' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201409' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201408' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201407' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201406' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201405' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201404' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201403' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201402' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201401' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201312' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201311' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201310' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201309' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201308' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201307' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201306' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201305' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201304' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201303' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201302' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201301' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201212' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201211' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201210' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201209' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201208' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201207' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201206' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201205' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201204' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201203' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201202' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201201' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201112' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201111' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201110' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201109' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201108' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201107' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201106' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201105' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201104' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201103' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201102' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201101' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201012' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201011' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201010' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201009' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201008' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201007' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201006' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201005' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201004' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201003' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201002' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '201001' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200912' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200911' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200910' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200909' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200908' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200907' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200906' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200905' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200904' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200903' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200902' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200901' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200812' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200811' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200810' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200809' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200808' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200807' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200806' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200805' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200804' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200803' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200802' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200801' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200712' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200711' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200710' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200709' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200708' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200707' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200706' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200705' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200704' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200703' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200702' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200701' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200612' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200611' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200610' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200609' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200608' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200607' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200606' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200605' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200604' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200603' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200602' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200601' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200512' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200511' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200510' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200509' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200508' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200507' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200506' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200505' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200504' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200503' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200502' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200501' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200412' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200411' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200410' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200409' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200408' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200407' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200406' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200405' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200404' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200403' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200402' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200401' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200312' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200311' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200310' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200309' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200308' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200307' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200306' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200305' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200304' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200303' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200302' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200301' THEN 50
            when to_char(mod_dtm, 'YYYYMM') = '200212' THEN 50
        END num_partition,
        ORD_ITEM_ID
         ,  REG_DTM
         ,  REGR_ID
         ,  MOD_DTM
         ,  MODR_ID
         ,  ITEM_ORD_DT
         ,  ORD_NO
         ,  ORD_ITEM_NO
         ,  BEF_ORD_NO
         ,  BEF_ORD_ITEM_ID
         ,  BEF_ORD_ITEM_NO
         ,  ORG_ORD_ITEM_ID
         ,  ORG_ORD_DTM
         ,  EXCH_PAIR_ORD_ITEM_ID
         ,  AS_ORD_NO
         ,  PROPRD_ORG_ORD_ITEM_ID
         ,  LINE_TYP_CD
         ,  ST_CD
         ,  ST_CHG_DTM
         ,  FST_ORD_CNF_PRSN_ID
         ,  ITEM_WORK_ST_NM
         ,  ITEM_WORK_ST_CD
         ,  ITEM_VALID_YN
         ,  ORD_PSBL_CHK_EXCPT_YN
         ,  MOD_YN
         ,  CNL_YN
         ,  MULTI_CD
         ,  CHANL_CD
         ,  CHANL_DTL_CD
         ,  PRD_CD
         ,  REPLACE(REPLACE(PRD_NM, CHR(10), ''), CHR(13), '') PRD_NM
         ,  ATTR_PRD_CD
         ,  STD_UPRC
         ,  LAST_UPRC
         ,  PRD_NO_INT_INSM_MM
         ,  ORD_QTY
         ,  TMP_QTY
         ,  RTP_QTY
         ,  RTP_PSBL_QTY
         ,  RTP_SCHD_QTY
         ,  EXCH_QTY
         ,  EXCH_RTP_WORK_YN
         ,  RTP_RE_REQ_PREVNT_CD
         ,  STOCK_ORD_YN
         ,  ORD_QTY_CHK_YN
         ,  DLVP_ADDR_NO
         ,  RSN_LRG_CLS_CD
         ,  RSN_MID_CLS_CD
         ,  RSN_SML_CLS_CD
         ,  PLEIN_RTP_RSN_CD
         ,  DLV_PICK_MTHOD_CD
         ,  DIRDLV_CHG_YN
         ,  EXCHRG_DLVS_CD
         ,  DLVS_CO_CD
         ,  DLVS_CO_TRMNL_NM
         ,  DLVS_CO_BRN_NM
         ,  DLVS_CO_BRN_CD
         ,  SHIP_BRN_CD
         ,  INV_NO
         ,  INV_CNF_SUBJ_CD
         ,  FTHLD_GATHRPRD_DLVS_CO_CD
         ,  FTHLD_GATHRPRD_INV_NO
         ,  CUST_SND_YN
         ,  CUST_SND_INV_NO
         ,  CUST_SND_DLVS_CO_CD
         ,  SUPLY_PLAN_DT_APPLY_YN
         ,  SUPLY_PLAN_DT
         ,  SUPLY_PLAN_BROAD_DT
         ,  SUPLY_PLAN_DLV_SCHD_DT
         ,  CATV_STD_RELS_DDCNT
         ,  DM_STD_RELS_DDCNT
         ,  EC_STD_RELS_DDCNT
         ,  DLV_PLAN_DT
         ,  FST_DLV_ATEMP_DT
         ,  RELS_SCHD_DT
         ,  SUP_RELS_SCHD_DT
         ,  DLV_SCHD_DT
         ,  TH2_DLV_SCHD_DT
         ,  CHG_DLV_SCHD_DT
         ,  BROAD_DLV_SCHD_DT_CNTNT
         ,  EC_DLV_DT_GUIDE_YN
         ,  EC_DLV_SCHD_DT
         ,  EC_DIRDLV_PRD_DLV_SCHD_DT
         ,  EC_RELS_OBEY_DT
         ,  EC_AVG_DLV_DDCNT
         ,  EC_VALID_DLV_CD
         ,  EC_DLY_YN
         ,  SHIP_DIR_DT
         ,  RELS_FSH_DT
         ,  DLVS_CO_RELS_FSH_DT
         ,  DLV_FSH_DT
         ,  DLV_FSH_SUBJ_CD
         ,  DLV_SCHD_DT_CHG_RSN_CD
         ,  DLV_DLY_RSN_CD
         ,  BILL_DT
         ,  BILL_PROC_SUBJ_CD
         ,  BILL_PROC_DT
         ,  RTP_PICK_PRG_ST_CHG_DTM
         ,  RTP_PRD_PICK_ST_CHG_DTM
         ,  RTP_IST_FSH_ST_CHG_DTM
         ,  DIRDLV_PICK_DIR_YN
         ,  APNT_DLVS_PICK_YN
         ,  APNT_DLVS_PICK_SUP_ADDR_NO
         ,  CVS_PICK_CHG_DT
         ,  CVS_ACP_DT
         ,  CVS_NM
         ,  CVS_APRV_NO
         ,  CHR_DLV_YN
         ,  DLVC_GBN_CD
         ,  DLVC_STD_AMT
         ,  OBOX_CD
         ,  DIRDLV_OBOX_DLVC_IMPOSE_YN
         ,  DIRDLV_OBOX_DLVC_CD
         ,  DIRDLV_OBOX_DLV_ST_CD
         ,  EXCH_RTPC_IMPOSE_YN
         ,  RTP_DLVC_IMPOSE_AMT
         ,  EXCH_RTPC_ORD_ITEM_ID
         ,  PLEIN_RTP_DLVC_ORD_ITEM_ID
         ,  REP_PRD_SUP_PRD_CD
         ,  REP_PRD_SUP_PRD_NM
         ,  REP_PRD_SUP_ATTR_PRD_NM
         ,  EXPOS_PMO_NM
         ,  EXPOS_PRD_NM
         ,  EXPOS_PR_SNTNC_NM
         ,  ASIST_NEED_YN
         ,  OPT_PRD_TYP_CD
         ,  ORD_MNFC_YN
         ,  DITTO_YN
         ,  DITTO_TMA_CD
         ,  DITTO_BUNDL_DLV_LIMIT_YN
         ,  OPER_MD_ID
         ,  PRCH_PRC
         ,  PRCH_TYP_CD
         ,  SUP_GIV_RTAMT
         ,  SUP_GIV_RTAMT_CD
         ,  SUP_PROPRD_UPRC
         ,  TAX_TYP_CD
         ,  ASUMP_CNTRB_PROFIT_AMT
         ,  SUP_CD
         ,  BROAD_PRD_FORM_ID
         ,  BROAD_LIVBROD_ORD_YN
         ,  BROAD_FEE_APPLY_YN
         ,  BROAD_END_DT
         ,  PRE_ORD_BROAD_DT
         ,  PRE_ORD_TYP_CD
         ,  BROAD_PRE_ORD_PATH_NM
         ,  BROAD_PRE_ORD_BROAD_ID
         ,  DM_SEQNO_ID
         ,  CHAR_CPN_TYP_CD
         ,  TAX_INV_ISSUE_YN
         ,  EC_EXPOS_EXCPT_YN
         ,  EC_ALIA_CALC_YN
         ,  EC_LIVBROD_YN
         ,  EC_SUP_ORD_NO
         ,  PLEIN_ORD_ST_CD
         ,  PLEIN_SET_PRD_ATTR_PRD_CD_1
         ,  PLEIN_SET_PRD_ATTR_PRD_CD_2
         ,  PLEIN_OBOX_NO
         ,  PLEIN_FORNMNY_CURRUN_CD
         ,  PLEIN_SUP_GIV_FORNMNY_AMT
         ,  PLEIN_INTRNAT_TRPT_FEE
         ,  PLEIN_ONSITE_INDIVI_PRC
         ,  PLEIN_ONSITE_DC_PRC_USD_AMT
         ,  PLEIN_ONSITE_TAX_USD_AMT
         ,  PLEIN_TARIF_VAT
         ,  PLEIN_BEFRTP_COST
         ,  PLEIN_BEFRTP_SUP_GIV_AMT
         ,  PLEIN_BEFRTP_SUP_GIV_USD_AMT
         ,  PLEIN_AFTRTP_COST
         ,  PLEIN_AFTRTP_SUP_GIV_AMT
         ,  PLEIN_AFTRTP_SUP_GIV_USD_AMT
         ,  TC_DMC_ID
         ,  TC_GBN_CD
         ,  TC_MAIN_ID
         ,  TC_MAIN_MENU_SEQ
         ,  TC_MENU_ID
         ,  TC_CTGR_ID
         ,  TC_CONR_ID
         ,  DSTRB_CENT_IN_AS_YN
         ,  WTH_LAST_REG_DTM
         ,  WTH_ORD_CNF_CD
         ,  WTH_ORD_CNF_DTM
         ,  GSNPNT_MEMSHP_ADM_ST_CD
         ,  ACCM_NO_GIV_YN
         ,  GSNPNT_NO_GIV_YN
         ,  FST_ACCM_USE_AMT
         ,  ACC_CRE_STD_AMT
         ,  GFT_CPRC_TOT_AMT
         ,  PRD_CPN_MAX_DC_AMT
         ,  SHTPRD_ACCM_GIV_CD
         ,  CENT_IST_ARFN_YN
         ,  RFN_TYP_CD
         ,  ARFN_TIME_CD
         ,  ARFN_ST_CD
         ,  ARFN_AUTO_RFN_SCHD_DT
         ,  ARFN_DT
         ,  ARFN_CNF_DT
         ,  ARFN_RTN_DT
         ,  ARFN_RTN_RSN_PRD_INSPPRD_CD
         ,  ARFN_RTN_RSN_INV_CNF_CD
         ,  ARFN_VR_QTY
         ,  ORD_CNF_IDEN_NO
         ,  SAP_IF_ST_CD
         ,  ORD_DLV_GRD_CD
         ,  APNT_DLV_DT
         ,  SUPLY_PLAN_QTY_FORM_YN
         ,  PRIM_ACT_MOD_DTM
         ,  PRIM_ACT_MODR_ID
         ,  PMO_EVENT_KIND_CD
         ,  GS25_PRD_YN
         ,  GS25_BRN_CD
         ,  CHAR_CPN_MSG_TITLE_NM
         ,  BUNDL_DLV_CD
         ,  ATTR_GFT_YN
         ,  ATTR_GFT_CONCT_YN
         ,  ARS_YN
         ,  SAP_ORDNG_NO
         ,  PRD_FMLY_DC_LIMIT_YN
         ,  EC_ATTR_SEQ
         ,  ACCM_GIV_TOT_AMT
         ,  RSN_CD_CHG_DTM
         ,  SUP_RELS_SCHD_CHG_DTM
         ,  ACC_GSHS_SHR_AMT
         ,  ACC_SUP_SHR_AMT
         ,  DM_PMO_1_APPLY_YN
         ,  DM_PMO_1_APPLY_WORKR_ID
         ,  DM_PMO_1_APPLY_WORK_DTM
         ,  DM_PMO_2_APPLY_YN
         ,  DM_PMO_2_APPLY_WORKR_ID
         ,  DM_PMO_2_APPLY_WORK_DTM
         ,  DM_PMO_3_APPLY_YN
         ,  DM_PMO_3_APPLY_WORKR_ID
         ,  DM_PMO_3_APPLY_WORK_DTM
         ,  DM_PMO_4_APPLY_YN
         ,  DM_PMO_4_APPLY_WORKR_ID
         ,  DM_PMO_4_APPLY_WORK_DTM
         ,  MULTI_SIMPL_GBN_CD
         ,  PRD_PMO_SEQ
         ,  SET_PRD_CD
         ,  SET_PRD_ORD_SEQ
         ,  SET_PRD_NM
         ,  GFT_MAND_YN
         ,  PMO_OFFER_SEQ
         ,  SET_PRD_MULTI_CD
         ,  ATTR_PRD_REP_CD
         ,  ORG_ORD_NO
         ,  PLEIN_FORGN_PRD_CD
         ,  BUNDL_DLV_GRP_CD
         ,  ARS_BROAD_CHK_YN
         ,  SAP_WORK_ST_NM
         ,  SAP_WORK_ST_CD
         ,  SUP_AGNCY_NM
         ,  GFT_INDIVI_DLV_PMSN_YN
         ,  RSRV_SALE_PRD_YN
         ,  INSTL_PRD_YN
         ,  PLEIN_DLV_INTRNAT_TRPT_FEE
         ,  PLEIN_SET_PRD_ATTR_DC_AMT_1
         ,  PLEIN_SET_PRD_ATTR_DC_AMT_2
         ,  DLV_PLAN_DT_EXPOS_EXCPT_YN
         ,  RSRV_ORD_DLV_PLAN_DT_GUIDE_YN
         ,  ORD_MNFC_AGREE_DTM
         ,  ORD_MNFC_AGREE_YN
         ,  ORD_MNFC_TERM_DDCNT
         ,  ORD_MNFC_TYP_CD
         ,  EC_ATTR_PRD_CD
         ,  DIRDLV_CHG_CHG_DTM
         ,  DIRDLV_CHG_MODR_ID
         ,  RELS_TNS_DTM
         ,  TMP_ORD_YN
         ,  ALIA_TRMS_TYP_CD
         ,  MACHN_CD
         ,  DLV_EMP_NM
         ,  ALIA_CALC_DTM
         ,  APP_GBN_CD
         ,  DEAL_NO
         ,  PLEIN_ORD_PRSN_ENG_NM                                         
         ,  PLEIN_RCVR_ENG_NM                                             
         ,  GSHS_PICK_YN
        FROM smtc_own.ord_item_d A
    ) 
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
                .option("lowerBound", lowerBound)
                .option("upperBound", upperBound)
                .option("fetchsize", fetchsize)
                .load()
    )
                # .option("dateFormat", "YYYY-MM-DD HH24:MI:SS" )
                # .option("oracle.jdbc.mapDateToTimestamp", "false")
                # .option("sessionInitStatement", "ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'")

    # print(f"########## {df.count()}")

    output_path = f"s3://s3-clickstream-test-01/tmp/dsmtcdb12/smtc_own.ord_item_d/"

    # S3에 Parquet 포맷으로 저장
    df.write \
        .mode("append") \
        .parquet(output_path)


    spark.stop()