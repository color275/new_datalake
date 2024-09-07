from django.db import connections
from ..models import *

def get_or_create_table_metadata(db_name: str, table_name: str, db_id: int = 7):
    columns_query = f"""
        SELECT COLUMN_NAME, DATA_TYPE
        FROM ALL_TAB_COLUMNS
        WHERE OWNER||'.'||TABLE_NAME = '{table_name.upper()}'
    """
    
    pk_query = f"""
        SELECT COL.COLUMN_NAME
        FROM ALL_CONS_COLUMNS COL
        JOIN ALL_CONSTRAINTS CON
        ON COL.CONSTRAINT_NAME = CON.CONSTRAINT_NAME
        WHERE CON.CONSTRAINT_TYPE = 'P'
        AND CON.OWNER||'.'||COL.TABLE_NAME = '{table_name.upper()}'
    """
    
    with connections[db_name.db_name].cursor() as cursor:
        cursor.execute(columns_query)
        columns = cursor.fetchall()
        
        cursor.execute(pk_query)
        pk_columns = [pk[0] for pk in cursor.fetchall()]

    table, created = Tables.objects.get_or_create(
        table_name=table_name,
        defaults={
            'id_db': db_id,
            'catalog_db_name': db_name,
            'catalog_table_name': table_name,
            'comments': f"{table_name} 테이블의 논리명"
        }
    )

    for column_name, data_type in columns:
        data_type_obj = DataTypes.objects.filter(name=data_type).first()
        pk_yn = 'Y' if column_name in pk_columns else 'N'
        
        Columns.objects.get_or_create(
            id_table=table,
            column_name=column_name,
            defaults={
                'pk_yn': pk_yn,
                'partition_yn': 'N',
                'id_datatypes': data_type_obj,
                'comments': f"{column_name} 컬럼의 논리명"
            }
        )
    return table