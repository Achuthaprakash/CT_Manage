# Generated by Django 2.2.5 on 2019-12-25 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kaju', '0017_auto_20191225_1052'),
    ]

    operations = [
        migrations.RenameField(
            model_name='processing_lot',
            old_name='final_ouput',
            new_name='final_output',
        ),
    ]
