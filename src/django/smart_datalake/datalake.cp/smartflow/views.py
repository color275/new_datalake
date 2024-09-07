from rest_framework import viewsets
from rest_framework.response import Response
from .models import Tables
from .serializers import *
from rest_framework.views import APIView
from django.db import connection


class GetTableInfoByIntervalView(APIView):
    def get(self, request, *args, **kwargs):
        interval_type = request.query_params.get('interval_type', None)

        if not interval_type:
            return Response({"error": "interval_type name is required"}, status=400)

        with connection.cursor() as cursor:
            # SQL 쿼리 작성
            cursor.execute("""
SELECT 
    d.db_name, 
    dt.db_type_name AS db_type,
    d.host,
    d.port,
    d.options,
    t.table_name, 
    t.sql_where,
    li.interval_type,
    lm.load_type,
    e.db_env_name AS env_name,
    d.bucket_path,
    d.cdc_bucket_path,
    t.catalog_db_name,
    t.catalog_table_name,
    t.spark_num_executors,
    t.spark_executor_cores,
    CONCAT(t.spark_executor_memory, 'g') AS spark_executor_memory,
    t.spark_partitionColumn,
    t.spark_lowerBound,
    t.spark_upperBound,
    t.spark_numpartitions,
    t.spark_fetchsize,
    t.spark_query,
    t.cdc_yn,
    t.use_yn,
    GROUP_CONCAT(c.column_name ORDER BY c.id) AS columns,
    GROUP_CONCAT(IF(c.pk_yn = 'Y', c.column_name, NULL) ORDER BY c.id) AS primary_keys,
    COALESCE(GROUP_CONCAT(IF(c.partition_yn = 'Y', c.column_name, NULL) ORDER BY c.id), '') AS partition_columns
FROM 
    sf_databases d
    JOIN sf_database_types dt ON d.id_databasetype = dt.id
    JOIN sf_tables t ON d.id = t.id_db
    JOIN sf_columns c ON t.id = c.id_table    
    JOIN sf_load_interval li ON li.id = t.id_load_interval
    JOIN sf_load_method lm ON lm.id = t.id_load_method
    JOIN sf_db_env e ON d.id_dbenv = e.id
WHERE 
    li.interval_type = %s
GROUP BY 
    d.db_name, dt.db_type_name, d.host, d.port, 
    d.options, t.table_name, d.bucket_path, d.cdc_bucket_path, 
    t.sql_where, li.interval_type, lm.load_type, e.db_env_name, 
    t.catalog_db_name, t.catalog_table_name, 
    t.spark_num_executors, t.spark_executor_cores, 
    t.spark_executor_memory, t.cdc_yn, t.use_yn,
                           t.spark_partitionColumn,
    t.spark_lowerBound,
    t.spark_upperBound,
    t.spark_numpartitions,
    t.spark_fetchsize,
    t.spark_query
            """, [interval_type])

            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]

            # 컬럼, 소스 데이터 타입, 매핑된 데이터 타입을 리스트로 변환
            for row in result:
                row['columns'] = row['columns'].split(',')
                row['primary_keys'] = row['primary_keys'].split(',')
                row['partition_columns'] = row['partition_columns'].split(',')

        return Response(result)

    
# class TablesViewSet(viewsets.ModelViewSet):
#     serializer_class = TablesSerializer

#     def get_queryset(self):
#         table_name = self.request.query_params.get('table_name', None)
#         if table_name is not None:
#             return Tables.objects.filter(table_name=table_name)
#         return Tables.objects.all()
