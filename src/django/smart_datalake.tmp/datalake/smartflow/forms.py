from django import forms

class TableMetadataForm(forms.Form):
    db_name = forms.CharField(label='Database Name', max_length=100)
    table_name = forms.CharField(label='Table Name', max_length=100)