# Generated by Django 2.2.5 on 2019-12-22 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kaju', '0012_auto_20191222_1046'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cutting_section',
            old_name='lot_name',
            new_name='processing_lot',
        ),
    ]
