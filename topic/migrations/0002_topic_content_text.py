# Generated by Django 4.1.1 on 2022-10-24 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='content_text',
            field=models.TextField(default='<p>hello</p>', verbose_name='带样式的文章内容'),
            preserve_default=False,
        ),
    ]
