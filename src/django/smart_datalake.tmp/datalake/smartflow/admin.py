from django.contrib import admin
from .models import *
import datetime


class BaseAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        all_fields = [field.name for field in model._meta.fields]
        priority_fields = ['mod_dtm', 'id_mod_user']
        self.list_display = [
            field for field in all_fields if field not in priority_fields] + priority_fields
        self.fields = [field for field in all_fields if field not in [
            'id', 'mod_dtm', 'id_mod_user']]
        super().__init__(model, admin_site)

    def save_model(self, request, obj, form, change):
        obj.id_mod_user = request.user
        obj.mod_dtm = datetime.datetime.now()
        obj.save()


@admin.register(DbEnv)
class DbEnvAdmin(BaseAdmin):
    list_display_links = ['db_env_name']
    search_fields = ('db_env_name',)
    list_filter = ('db_env_name',)


@admin.register(DatabaseType)
class DatabaseTypeAdmin(BaseAdmin):
    list_display_links = ['db_type_name']
    search_fields = ('db_type_name',)
    list_filter = ('db_type_name',)


@admin.register(Databases)
class DatabasesAdmin(BaseAdmin):
    list_display_links = ['db_name']
    search_fields = ('db_name', 'db_type')
    list_filter = ('mod_dtm', 'id_dbenv')


@admin.register(LoadInterval)
class LoadIntervalAdmin(BaseAdmin):
    list_display_links = ['interval_type',]
    search_fields = ('interval_type',)
    list_filter = ('interval_type',)


@admin.register(LoadMethod)
class LoadMethodAdmin(BaseAdmin):
    list_display_links = ['load_type',]
    search_fields = ('load_type',)
    list_filter = ('load_type',)


class ColumnsInline(admin.TabularInline):
    model = Columns
    extra = 1
    exclude = ['mod_dtm', 'id_mod_user']


@admin.register(Tables)
class TablesAdmin(BaseAdmin):
    list_display_links = ['table_name']
    search_fields = ('table_name', 'owner')
    list_filter = ('cdc_yn', 'mod_dtm', 'id_db')

    inlines = [ColumnsInline]

    def save_related(self, request, form, formsets, change):
        form.save(commit=False)
        for formset in formsets:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.id_mod_user = request.user
                instance.mod_dtm = datetime.datetime.now()
                instance.save()
            formset.save_m2m()
        form.save_m2m()

    # def save_model(self, request, obj, form, change):
    #     if change:
    #         obj.id_mod_user = request.user
    #         obj.mod_dtm = datetime.datetime.now()
    #     else:
    #         obj.id_reg_user = request.user
    #     obj.save()

@admin.register(DataTypes)
class DataTypesAdmin(BaseAdmin):
    list_display_links = ['datatype_name']
    search_fields = ('datatype_name',)
    


@admin.register(DataTypesMapping)
class DataTypesMappingAdmin(BaseAdmin):
    list_display_links = ['datatype_mapping_name']
    search_fields = ('datatype_mapping_name',)
    


# @admin.register(Columns)
# class ColumnsAdmin(BaseAdmin):
#     list_display_links = ['column_name']
#     search_fields = ('column_name',)
    
