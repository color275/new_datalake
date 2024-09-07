from django.urls import path, include
from rest_framework import routers
from .views import *
from .admin import metadata_admin_site

urlpatterns = [
    # path('', include(router.urls)),
    path('get_table_info_by_interval/', GetTableInfoByIntervalView.as_view(), name='get_table_info_by_interval'),
    path('metadata-admin/', metadata_admin_site.urls),
    
]
