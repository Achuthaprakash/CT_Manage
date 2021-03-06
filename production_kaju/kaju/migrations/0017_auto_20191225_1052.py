# Generated by Django 2.2.5 on 2019-12-25 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kaju', '0016_auto_20191224_0710'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='climate_params',
            options={'ordering': ['-date_climate']},
        ),
        migrations.AlterModelOptions(
            name='processing_lot',
            options={'ordering': ['-lot_id']},
        ),
        migrations.CreateModel(
            name='peeling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peeled_wholes', models.FloatField()),
                ('peeled_pieces', models.FloatField()),
                ('unpeeled_wholes', models.FloatField()),
                ('unpeeled_pieces', models.FloatField()),
                ('rejections', models.FloatField()),
                ('husk', models.FloatField()),
                ('peeling_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kaju.climate_params')),
                ('peeling_lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kaju.processing_lot')),
            ],
        ),
    ]
