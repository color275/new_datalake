from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    mod_dtm = models.DateTimeField('수정일자', 
                                    blank=True, 
                                    null=True)
    id_mod_user = models.ForeignKey(User, 
                                    verbose_name='수정자', 
                                    null=True, 
                                    on_delete=models.DO_NOTHING,
                                    blank=True, 
                                    db_column='id_mod_user',
                                    related_name="%(class)s_mod_users")

    class Meta:
        abstract = True


class DbEnv(BaseModel):
    env_name = models.CharField('운영/테스트/개발', max_length=100)

    class Meta:
        verbose_name = '[DB] 운영/테스트/개발'
        verbose_name_plural = '[DB] 운영/테스트/개발'
        db_table = 'sf_db_env'

    def __str__(self):
        return self.env_name


class DatabaseType(BaseModel):
    name = models.CharField('DB 종류', max_length=100, unique=True)
    description = models.CharField('설명', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = '[DB] 데이터베이스 종류'
        verbose_name_plural = '[DB] 데이터베이스 종류'
        db_table = 'sf_database_types'

    def __str__(self):
        return self.name

class Databases(BaseModel):
    id_dbenv = models.ForeignKey(DbEnv,
                                 verbose_name="운영/테스트/개발",
                                 on_delete=models.CASCADE,
                                 db_column='id_dbenv')
    db_name = models.CharField('DB명', max_length=100)
    id_databasetype = models.ForeignKey(DatabaseType,
                                verbose_name="DB 종류",
                                on_delete=models.CASCADE,
                                db_column='id_databasetype',
                                null=True)
    host = models.CharField('호스트', max_length=255)
    port = models.IntegerField('포트')
    username = models.CharField('사용자명', max_length=100)
    password = models.CharField('비밀번호', max_length=100)
    options = models.JSONField('추가 옵션', blank=True, null=True)

    class Meta:
        verbose_name = '[DB] 데이터베이스'
        verbose_name_plural = '[DB] 데이터베이스'
        db_table = 'sf_databases'

    def __str__(self):
        return self.db_name


class LoadInterval(BaseModel):
    interval_type = models.CharField(
        '스케줄 타입', max_length=100)

    class Meta:
        verbose_name = '[스케줄] 로드 주기'
        verbose_name_plural = '[스케줄] 로드 주기'
        db_table = 'sf_load_interval'

    def __str__(self):
        return self.interval_type

class Tables(BaseModel):
    id_db = models.ForeignKey(Databases,
                              verbose_name='DB명',
                              on_delete=models.CASCADE,
                              db_column='id_db',
                              blank=True,
                              null=True,
                              default=7)
    table_name = models.CharField('테이블 물리명', max_length=100)
    comments = models.CharField(
        '테이블 논리명', max_length=200, blank=True, null=True)
    id_load_interval = models.ForeignKey(LoadInterval,
                                         verbose_name='로드 주기',
                                         on_delete=models.SET_NULL,
                                         db_column='id_load_interval',
                                         null=True,
                                         blank=True)
    cdc_yn = models.CharField('CDC 여부', max_length=1, choices=[
                              ('Y', 'Yes'), ('N', 'No')], default='N')
    sql_where = models.TextField('SQL WHERE 절', blank=True, null=True)

    class Meta:
        verbose_name = '[DB] 테이블'
        verbose_name_plural = '[DB] 테이블'
        db_table = 'sf_tables'

    def __str__(self):
        return self.table_name


class DataTypes(BaseModel):
    name = models.CharField('데이터 타입 명', max_length=50, unique=True)
    description = models.CharField('설명', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = '[DB] 데이터 타입'
        verbose_name_plural = '[DB] 데이터 타입'
        db_table = 'sf_datatypes'

    def __str__(self):
        return self.name


class DataTypesMapping(BaseModel):
    name = models.CharField('데이터 타입 명', max_length=50, unique=True)

    class Meta:
        verbose_name = '[DB] 매핑 데이터 타입'
        verbose_name_plural = '[DB] 매핑 데이터 타입'
        db_table = 'sf_datatypes_mapping'

    def __str__(self):
        return self.name


class Columns(BaseModel):
    id_table = models.ForeignKey(Tables,
                                 verbose_name='테이블',
                                 on_delete=models.CASCADE,
                                 db_column='id_table')
    column_name = models.CharField('컬럼 물리명', max_length=100)
    id_datatypes = models.ForeignKey(DataTypes,
                                     verbose_name='데이터 타입',
                                     on_delete=models.CASCADE,
                                     db_column='id_datatypes')
    id_datatypes_mapping = models.ForeignKey(DataTypesMapping,
                                             verbose_name='매핑 타입',
                                             on_delete=models.CASCADE,
                                             db_column='id_datatypes_mapping')
    comments = models.CharField(
        '컬럼 논리명', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = '[DB] 컬럼'
        verbose_name_plural = '[DB] 컬럼'
        db_table = 'sf_columns'

    def __str__(self):
        return self.column_name
