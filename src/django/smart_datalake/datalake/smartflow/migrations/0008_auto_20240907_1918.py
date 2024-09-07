# Generated by Django 3.2.25 on 2024-09-07 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartflow', '0007_auto_20240907_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='columns',
            name='use_yn',
            field=models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='Y', max_length=1, verbose_name='사용 여부'),
        ),
        migrations.AlterField(
            model_name='columns',
            name='id_table',
            field=models.ForeignKey(db_column='id_table', on_delete=django.db.models.deletion.CASCADE, to='smartflow.tables', verbose_name='테이블'),
        ),
        migrations.AlterField(
            model_name='databases',
            name='db_name',
            field=models.CharField(max_length=100, verbose_name='이름(SMTC,WEBDB)'),
        ),
    ]