import cx_Oracle
import psycopg2
from ..models import Databases, Tables, Columns

def get_or_create_table_metadata(db_id: int, table_name: str):
    # Databases 모델에서 해당 id의 DB 정보를 가져옴
    try:
        database = Databases.objects.get(id=db_id)
    except Databases.DoesNotExist:
        error_message = f"'{database}'에 해당하는 데이터베이스가 존재하지 않습니다."
        print(error_message)  # 콘솔에 에러 메시지 출력
        raise ValueError(error_message)

    # 테이블이 이미 존재하는지 확인
    table_instance = Tables.objects.filter(table_name=table_name.lower(), id_db=database).first()
    
    # 테이블이 존재하고 컬럼 정보가 하나라도 있으면 중지
    if table_instance and Columns.objects.filter(id_table=table_instance).exists():
        error_message = f"테이블 '{table_name}'에 컬럼 정보가 이미 존재합니다."
        print(error_message)  # 콘솔에 에러 메시지 출력
        return  # 함수 종료

    # DB 타입에 따라 연결 및 쿼리 실행 로직 분기
    if database.id_databasetype.db_type_name == 'Oracle':
        connection_string = f"{database.username}/{database.password}@{database.host}:{database.port}/{database.sid}"
        conn = cx_Oracle.connect(connection_string)
    elif database.id_databasetype.db_type_name == 'PostgreSQL':
        connection_string = f"host={database.host} port={database.port} dbname={database.sid} user={database.username} password={database.password}"
        conn = psycopg2.connect(connection_string)
    else:
        error_message = f"지원되지 않는 데이터베이스 유형입니다: {database.id_databasetype.db_type_name}"
        print(error_message)
        return

    try:
        cursor = conn.cursor()

        if database.id_databasetype.db_type_name == 'Oracle':
            # 테이블 존재 여부를 확인하는 Oracle 쿼리
            cursor.execute(f"""
                SELECT COUNT(*)
                FROM all_tables
                WHERE owner||'.'||table_name = UPPER('{table_name}')
            """)
            table_exists = cursor.fetchone()[0]

            if table_exists == 0:
                error_message = f"테이블 '{table_name}'이(가) 데이터베이스에 존재하지 않습니다."
                print(error_message)  # 콘솔에 에러 메시지 출력
                return  # 테이블이 존재하지 않으면 함수 종료

            # 테이블의 코멘트를 가져오는 Oracle 쿼리
            cursor.execute(f"""
                SELECT comments
                FROM all_tab_comments
                WHERE owner||'.'||table_name = UPPER('{table_name}')
            """)
            table_comment = cursor.fetchone()
            table_comment = table_comment[0] if table_comment else f'{table_name}의 메타데이터'

            print(f"# {table_comment}")

            # 컬럼 메타데이터를 가져오는 Oracle 쿼리
            cursor.execute(f"""
                SELECT column_name, data_type, nullable
                FROM all_tab_columns
                WHERE owner||'.'||table_name = UPPER('{table_name}')
                ORDER BY column_id
            """)
            columns = cursor.fetchall()

            # 컬럼 코멘트를 가져오는 Oracle 쿼리
            cursor.execute(f"""
                SELECT column_name, comments
                FROM all_col_comments
                WHERE owner||'.'||table_name = UPPER('{table_name}')
            """)
            column_comments = {row[0]: row[1] for row in cursor.fetchall()}  # 컬럼명과 코멘트 매핑

            # Primary Key 정보를 가져오는 Oracle 쿼리
            cursor.execute(f"""
                SELECT cols.column_name
                FROM all_constraints cons, all_cons_columns cols
                WHERE cons.constraint_type = 'P'
                AND cons.constraint_name = cols.constraint_name
                AND cons.owner = cols.owner
                AND cols.owner||'.'||cols.table_name = UPPER('{table_name}')
            """)
            primary_keys = [row[0] for row in cursor.fetchall()]

        elif database.id_databasetype.db_type_name == 'PostgreSQL':
            # 테이블 존재 여부를 확인하는 PostgreSQL 쿼리
            cursor.execute(f"""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema||'.'||table_name = LOWER('{table_name}')
            """)
            table_exists = cursor.fetchone()[0]

            if table_exists == 0:
                error_message = f"테이블 '{table_name}'이(가) 데이터베이스에 존재하지 않습니다."
                print(error_message)  # 콘솔에 에러 메시지 출력
                return  # 테이블이 존재하지 않으면 함수 종료

            # 테이블의 코멘트를 가져오는 PostgreSQL 쿼리
            cursor.execute(f"""
                SELECT obj_description(('"'||table_schema||'"."'||table_name||'"')::regclass, 'pg_class')
                FROM information_schema.tables
                WHERE table_schema||'.'||table_name = LOWER('{table_name}')
            """)
            table_comment = cursor.fetchone()
            table_comment = table_comment[0] if table_comment else f'{table_name}의 메타데이터'


            # 컬럼 메타데이터를 가져오는 PostgreSQL 쿼리
            cursor.execute(f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_schema||'.'||table_name = LOWER('{table_name}')
                ORDER BY ordinal_position
            """)
            columns = cursor.fetchall()

            # 컬럼 코멘트를 가져오는 PostgreSQL 쿼리
            cursor.execute(f"""
                SELECT column_name, col_description(('"'||table_schema||'"."'||table_name||'"')::regclass, ordinal_position)
                FROM information_schema.columns
                WHERE table_schema||'.'||table_name = LOWER('{table_name}')
            """)
            column_comments = {row[0]: row[1] for row in cursor.fetchall()}  # 컬럼명과 코멘트 매핑

            # Primary Key 정보를 가져오는 PostgreSQL 쿼리
            cursor.execute(f"""
                SELECT a.attname AS column_name
                FROM pg_index i
                JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
                JOIN pg_class c ON c.oid = i.indrelid
                JOIN pg_namespace n ON n.oid = c.relnamespace
                WHERE i.indisprimary
                AND n.nspname || '.' || c.relname = LOWER('{table_name}')
            """)
            primary_keys = [row[0] for row in cursor.fetchall()]

        # 테이블 정보가 존재하지 않으면 Tables에 새로 생성
        table_instance, created = Tables.objects.get_or_create(
            table_name=table_name.lower(),
            id_db=database,
            use_yn='N',
            defaults={'comments': table_comment}  # 테이블 코멘트 저장
        )

        # 컬럼 정보를 Columns에 저장
        for column in columns:
            column_name, data_type, nullable = column
            is_pk = 'Y' if column_name in primary_keys else 'N'
            column_comment = column_comments.get(column_name, f'{column_name} 컬럼')  # 컬럼 코멘트 저장

            Columns.objects.get_or_create(
                id_table=table_instance,
                column_name=column_name.lower(),
                defaults={
                    'pk_yn': is_pk,
                    'partition_yn': 'N',  # 필요에 따라 수정
                    'datatype': data_type.lower(),  # 데이터 타입을 Columns 모델의 datatype 필드에 저장
                    'comments': column_comment,
                }
            )

        print(f"테이블 '{table_name}'의 메타데이터가 성공적으로 추가되었습니다.")
    
    except Exception as e:
        print(f"메타데이터를 처리하는 중 오류 발생: {e}")
    
    finally:
        cursor.close()
        conn.close()