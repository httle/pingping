# Generated by Django 2.2 on 2019-04-28 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20190428_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='readed_num',
            field=models.IntegerField(default=0),
        ),
    ]
