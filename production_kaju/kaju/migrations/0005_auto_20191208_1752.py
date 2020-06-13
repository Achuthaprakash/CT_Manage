# Generated by Django 2.2.5 on 2019-12-08 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kaju', '0004_auto_20191208_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='bucket',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.CreateModel(
            name='RCN_drying',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_days', models.IntegerField()),
                ('moisture_after_drying', models.FloatField()),
                ('quantity_after', models.FloatField()),
                ('weight_loss', models.FloatField()),
                ('production_out_turn', models.FloatField()),
                ('nut_count_after', models.IntegerField()),
                ('bin_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kaju.bucket')),
            ],
        ),
    ]