# Generated by Django 2.2.5 on 2019-12-08 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaju', '0003_auto_20191208_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucket',
            name='bucket_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]