# Generated by Django 4.2.3 on 2023-08-10 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CropData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('commodity', models.CharField(default='Unknown', max_length=100)),
                ('variety', models.CharField(max_length=100)),
                ('classification', models.CharField(default='Crop', max_length=100)),
                ('category', models.CharField(default='Default Category', max_length=100)),
                ('high_price', models.FloatField()),
                ('low_price', models.FloatField()),
                ('time_variable', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='CropPricePrediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='files/')),
            ],
        ),
    ]
