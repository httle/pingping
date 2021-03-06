# Generated by Django 2.2.10 on 2020-03-11 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsnews', '0002_sportsnews_created_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='sportsnews',
            name='content',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='sportsnews',
            name='img',
            field=models.URLField(default=''),
        ),
        migrations.AddField(
            model_name='sportsnews',
            name='img_describe',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sportsnews',
            name='url',
            field=models.URLField(default=''),
        ),
    ]
