from django.contrib import admin
from .models import *
import datetime
from django.contrib import messages
from django.core.exceptions import ValidationError
from .forms import TableMetadataForm
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from .forms import *
from .utils.meta_utils import get_or_create_table_metadata




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

        has_primary_key = False
        for formset in formsets:
            instances = formset.save(commit=False)
            # 삭제된 객체 처리
            for deleted_instance in formset.deleted_objects:
                deleted_instance.delete()
            for instance in instances:
                instance.column_name = instance.column_name.lower()
                if instance.pk_yn == 'Y':
                    has_primary_key = True
                instance.id_mod_user = request.user
                instance.mod_dtm = datetime.datetime.now()
                instance.save()
            formset.save_m2m()

        has_primary_key = Columns.objects.filter(
            id_table=form.instance, pk_yn='Y').exists()

        if not has_primary_key:
            messages.error(
                request, f"DB '{form.instance.id_db.db_name}'의 테이블 '{form.instance.table_name}'에 Primary Key가 지정되지 않았습니다. 확인하세요.")

        form.save_m2m()

    def save_model(self, request, obj, form, change):
        obj.table_name = obj.table_name.lower()
        obj.id_mod_user = request.user
        obj.mod_dtm = datetime.datetime.now()
        super().save_model(request, obj, form, change)

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
    
# admin.py

class TableMetadataAdminSite(admin.AdminSite):
    site_header = 'Table Metadata Admin'
    site_title = 'Metadata Admin'
    index_title = 'Metadata Management'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add-metadata/', self.admin_view(self.add_metadata_view)),
        ]
        return custom_urls + urls

    def add_metadata_view(self, request):
        if request.method == 'POST':
            form = TableMetadataForm(request.POST)
            if form.is_valid():
                db_name = form.cleaned_data['db_name']
                table_name = form.cleaned_data['table_name']

                # get_or_create_table_metadata 실행
                try:
                    get_or_create_table_metadata(db_name, table_name)
                    self.message_user(request, f"Metadata for table '{table_name}' in database '{db_name}' has been added successfully.", messages.SUCCESS)
                    return HttpResponseRedirect("../")
                except Exception as e:
                    self.message_user(request, f"Error: {str(e)}", messages.ERROR)
                    return HttpResponseRedirect("../")
        else:
            form = TableMetadataForm()

        return render(request, 'admin/add_table_metadata.html', {'form': form})

# metadata_admin_site 인스턴스화
metadata_admin_site = TableMetadataAdminSite(name='metadata_admin')