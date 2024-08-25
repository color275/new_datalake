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
    dt.name AS db_type,
    d.host,
    d.port,
    d.username,
    d.password,
    d.options,
    t.table_name, 
    t.sql_where,
    li.interval_type,
    e.env_name,
    GROUP_CONCAT(c.column_name ORDER BY c.id) AS columns,
    GROUP_CONCAT(dt1.name ORDER BY c.id) AS data_types,
    GROUP_CONCAT(dt2.name ORDER BY c.id) AS data_types_mapping
FROM 
    sf_databases d,
    sf_database_types dt,
    sf_tables t,
    sf_columns c,
    sf_datatypes dt1,
    sf_datatypes_mapping dt2,
    sf_load_interval li,
    sf_db_env e
WHERE 
    d.id_databasetype = dt.id
    AND d.id = t.id_db
    AND t.id = c.id_table
    AND c.id_datatypes = dt1.id
    AND c.id_datatypes_mapping = dt2.id
    AND li.id = t.id_load_interval
    AND d.id_dbenv = e.id  -- 운영/개발 환경 조인
    AND li.interval_type = %s
GROUP BY 
    d.db_name, dt.name, d.host, d.port, d.username, 
    d.password, d.options, t.table_name, 
    t.sql_where, li.interval_type, e.env_name
            """, [interval_type])

            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]

            # 컬럼, 소스 데이터 타입, 매핑된 데이터 타입을 리스트로 변환
            for row in result:
                row['columns'] = row['columns'].split(',')
                row['data_types'] = row['data_types'].split(',')
                row['data_types_mapping'] = row['data_types_mapping'].split(
                    ',')

        return Response(result)

    
# class TablesViewSet(viewsets.ModelViewSet):
#     serializer_class = TablesSerializer

#     def get_queryset(self):
#         table_name = self.request.query_params.get('table_name', None)
#         if table_name is not None:
#             return Tables.objects.filter(table_name=table_name)
#         return Tables.objects.all()
