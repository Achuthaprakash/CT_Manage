# Generated by Django 2.2.5 on 2019-12-09 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kaju', '0006_climate_params_day_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='processes',
            fields=[
                ('pro_id', models.IntegerField(primary_key=True, serialize=False)),
                ('process', models.CharField(max_length=250)),
            ],
        ),
        migrations.AlterModelOptions(
            name='day_type',
            options={'ordering': ['day_type']},
        ),
        migrations.CreateModel(
            name='processing_lot',
            fields=[
                ('lot_id', models.IntegerField(primary_key=True, serialize=False)),
                ('lot_name', models.CharField(max_length=6)),
                ('quantity', models.FloatField()),
                ('bucket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kaju.bucket')),
                ('date_of_position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kaju.day_type')),
            ],
        ),
    ]