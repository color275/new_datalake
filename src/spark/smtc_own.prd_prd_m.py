from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os
from datetime import datetime, timedelta

if __name__ == '__main__':
    
    lowerBound = 1
    upperBound = 18
    numPartitions = 18

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
    table = "smtc_own.prd_prd_m"
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
            WHEN to_char(mod_dtm, 'YYYYMM') BETWEEN '200001' AND '200902' THEN 1
            WHEN to_char(mod_dtm, 'YYYYMM') BETWEEN '200903' AND '201001' THEN 2
            WHEN to_char(mod_dtm, 'YYYYMM') BETWEEN '201002' AND '201103' THEN 3
            WHEN to_char(mod_dtm, 'YYYYMM') BETWEEN '201104' AND '201205' THEN 4
            WHEN to_char(mod_dtm, 'YYYYMM') BETWEEN '201206' AND '201307' THEN 5
            WHEN to_char(mod_dtm, 'YYYYMM') BETWEEN '201308' AND '201408' THEN 6
            WHEN to_char(mod_dtm, 'YYYYMM') BETWEEN '201409' AND '201510' THEN 7
            WHEN to_char(mod_dtm, 'YYYYMM') BETWEEN '201511' AND '201612' THEN 8
            WHEN to_char(mod_dtm, 'YYYYMM') BETWEEN '201701' AND '201803' THEN 9
            WHEN to_char(mod_dtm, 'YYYYMM') BETWEEN '201804' AND '201905' THEN 10
            WHEN to_char(mod_dtm, 'YYYYMM') BETWEEN '201906' AND '202007' THEN 11
            WHEN to_char(mod_dtm, 'YYYYMM') BETWEEN '202008' AND '202109' THEN 12
            WHEN to_char(mod_dtm, 'YYYYMM') BETWEEN '202110' AND '202202' THEN 13
            WHEN to_char(mod_dtm, 'YYYYMM') BETWEEN '202203' AND '202302' THEN 14
            WHEN to_char(mod_dtm, 'YYYYMM') BETWEEN '202303' AND '202307' THEN 15
            WHEN to_char(mod_dtm, 'YYYYMM') BETWEEN '202308' AND '202310' THEN 16
            WHEN to_char(mod_dtm, 'YYYYMM') BETWEEN '202311' AND '202312' THEN 17
            WHEN to_char(mod_dtm, 'YYYYMM') >= '202401' THEN 18
        END num_partition,
        A.PRD_CD
        , A.REG_DTM
        , A.REGR_ID
        , A.MOD_DTM
        , A.MODR_ID
        , A.USE_YN
        , A.ITEM_CD
        , A.BRAND_CD
        , A.COPY_SRC_PRD_CD
        , A.COPY_PRD_YN
        , A.REP_PRD_CD
        , SUBSTRB(A.PRD_NM,  1,  80)  PRD_NM                               
        , A.AUTO_ORD_PRD_NM
        , A.PRD_ENG_NM
        , A.MNFC_CO_NM
        , A.ORGP_NM
        , A.MODEL_NO
        , A.PRD_CLS_CD
        , A.PRD_TYP_CD
        , A.PRD_GBN_CD
        , A.PRCH_TYP_CD
        , A.ORD_PRD_TYP_CD
        , A.FRMLES_PRD_TYP_CD
        , A.GFT_TYP_CD
        , A.TAX_TYP_CD
        , A.EXPOS_ST_CD
        , A.REP_PRD_YN
        , A.BUNDL_PRD_GBN_CD
        , A.SEPAR_ORD_NOADMT_YN
        , A.QA_GRD_CD
        , A.QA_PRG_ST_CD
        , A.SALE_PSBL_APRV_YN
        , A.PRD_APRV_ST_CD
        , A.TEMPOUT_YN
        , A.EC_APRV_ST_CD
        , A.PRD_CNSDR_ST_CD
        , A.TASK_TEAM_APRV_RSLT_CNTNT
        , A.PRCH_TYP_APRV_CD
        , A.ORD_LIMIT_QTY
        , A.INSTL_DLV_PRD_YN
        , A.GFTCERT_FACE_PRC
        , A.FLGD_PRC_EXPOS_YN
        , A.DC_MRK_GBN_CD
        , A.PRC_COMPR_TNS_CD
        , A.COMPR_PRC_MRK_YN
        , A.ZRWON_SALE_YN
        , A.BASE_ACCM_LIMIT_YN
        , A.SEL_ACCM_APPLY_YN
        , A.SEL_ACC_RT
        , A.IMM_ACCM_DC_LIMIT_YN
        , A.IMM_ACCM_DC_RT
        , A.CPN_MAX_DC_AMT
        , A.CPN_APPLY_TYP_CD
        , A.CPN_DC_AMT_EXPOS_YN
        , A.GSNPNT_NO_GIV_YN
        , A.ALIA_SPCLSAL_LIMIT_YN
        , A.CARD_USE_LIMIT_YN
        , A.ORD_MNFC_YN
        , A.ORD_MNFC_TERM_DDCNT
        , A.RSRV_SALE_PRD_YN
        , A.RSRV_ORD_PSBL_YN
        , A.SML_TYP_PRD_YN
        , A.ONAIR_SALE_PSBL_YN
        , A.IMBC_ALIA_YN
        , A.ADULT_CERT_YN
        , A.DITTO_YN
        , A.DITTO_BUNDL_DLV_LIMIT_YN
        , A.OPEN_AFT_RTP_NOADMT_YN
        , A.SUP_MOD_NOADMT_YN
        , A.BRAND_SHOP_DISP_YN
        , A.TAX_INV_ISSUE_YN
        , A.SPCLTAX_YN
        , A.ONETM_GIV_GFT_YN
        , A.IMG_CNF_YN
        , A.PRE_ORD_TYP_CD
        , A.PRE_ORD_BROAD_DT
        , A.AUTO_ORD_PSBL_YN
        , A.AUTO_ORD_CLS_CD
        , A.SUP_CD
        , A.SUB_SUP_CD
        , A.SUP_PRD_CD
        , A.MNFC_CO_GBN_CD
        , A.OPER_MD_ID
        , A.PRD_INFO_MNGR_ID
        , A.DLV_PICK_MTHOD_CD
        , A.PRD_RETP_ADDR_CD
        , A.PRD_RELSP_ADDR_CD
        , A.CVS_DLVS_RTP_YN
        , A.DLVS_CO_CD
        , A.OBOX_CD
        , A.CENT_ADD_PKG_YN
        , A.DLV_DT_GUIDE_CD
        , A.CHR_DLV_YN
        , A.CHR_DLVC_CD
        , A.IST_TYP_CD
        , A.CHR_DLV_ADD_YN
        , A.DLV_CRDIT_NO
        , A.PICK_CRDIT_NO
        , A.APNT_DLVS_IMPLM_YN
        , A.APNT_DLV_DLVS_CO_CD
        , A.APNT_PICK_DLVS_CO_CD
        , A.RFN_TYP_CD
        , A.ARFN_TIME_CD
        , A.EXCH_RTP_CHR_YN
        , A.RTP_DLVC_CD
        , A.RTP_ONEWY_RNDTRP_CD
        , A.EXCH_ONEWY_RNDTRP_CD
        , A.ATTR_TYP_NM1
        , A.ATTR_TYP_NM2
        , A.ATTR_TYP_NM3
        , A.ATTR_TYP_NM4
        , A.ATTR_TYP_SEQ_1
        , A.ATTR_TYP_SEQ_2
        , A.ATTR_TYP_SEQ_3
        , A.ATTR_TYP_SEQ_4
        , A.ATTR_TYP_EXPOS_CD
        , A.ATTR_PRD_PRC_YN
        , A.SALE_END_YN
        , A.SALE_END_PRSN_ID
        , A.SALE_END_RSN_CD
        , A.FST_EXPOS_DT
        , A.EXPOS_SCHD_DT
        , A.SAP_TNS_CD
        , A.PRD_REG_GBN_CD
        , A.BARCD_NO
        , A.INSU_CO_CD
        , A.PRD_BIT_ATTR_CD
        , A.GNUIN_YN
        , A.FLATPRC_PRD_YN
        , A.DM_SHTPRD_ALAM_YN
        , A.PRD_RESPNS_TGT_YN
        , A.GSHS_GFTCERT_YN
        , A.ARS_MAX_QTY
        , A.IF_YN
        , A.BROAD_PRD_YN
        , A.BUNDL_DLV_CD
        , A.REG_CHANL_GRP_CD
        , A.STYLE_DIR_ENT_YN
        , A.FORGN_PRD_NORM_PRC
        , A.ITEM_MAPPN_DTM
        , A.ORD_MNFC_TYP_CD
        , A.DLV_SCHD_DT_GUIDE_LIMIT_YN
        , A.DTCT_CD
        , A.ORGP_CD
        , A.FORGN_DLV_PSBL_YN
        , A.FORGN_DLV_WEIHT_VAL
        , A.PRC_MRK_TYP_VAL
        FROM smtc_own.prd_prd_m A
        -- WHERE mod_dtm > trunc(sysdate) - 365
    ) 
    -- WHERE num_partition in (1,2,3,4,5,6,7)
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

    output_path = f"s3://s3-clickstream-test-01/tmp/dsmtcdb12/smtc_own.prd_prd_m/"

    # S3에 Parquet 포맷으로 저장
    df.write \
        .mode("append") \
        .parquet(output_path)


    spark.stop()