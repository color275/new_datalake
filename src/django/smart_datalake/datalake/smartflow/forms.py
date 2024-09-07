from django import forms
from .models import Databases

class TableMetadataForm(forms.Form):
    db_name = forms.ModelChoiceField(queryset=Databases.objects.all(), label='DB명')
    table_name = forms.CharField(max_length=100, label='테이블명')