# Generated by Django 4.1.1 on 2024-04-29 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, verbose_name='权限编号')),
                ('name', models.CharField(max_length=100, verbose_name='权限名称')),
            ],
        ),
    ]
