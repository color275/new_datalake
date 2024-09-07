from django import forms
from .models import Databases, DbEnv

class TableMetadataForm(forms.Form):
    db_env = forms.ModelChoiceField(queryset=DbEnv.objects.all(), label='환경')
    db_name = forms.ModelChoiceField(queryset=Databases.objects.none(), label='DB명')
    table_name = forms.CharField(max_length=100, label='테이블명')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'db_env' in self.data:
            try:
                db_env_id = int(self.data.get('db_env'))
                self.fields['db_name'].queryset = Databases.objects.filter(id_dbenv=db_env_id)
            except (ValueError, TypeError):
                self.fields['db_name'].queryset = Databases.objects.none()
        else:
            self.fields['db_name'].queryset = Databases.objects.none()