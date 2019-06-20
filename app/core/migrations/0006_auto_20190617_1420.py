# Generated by Django 2.2.2 on 2019-06-17 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190617_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='title',
            field=models.CharField(db_index=True, max_length=50, unique=True),
        ),
    ]
