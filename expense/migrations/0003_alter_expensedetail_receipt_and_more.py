# Generated by Django 5.0.6 on 2024-05-31 08:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0002_detailuser'),
        ('trips', '0003_tripdetail_context'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensedetail',
            name='receipt',
            field=models.FileField(upload_to='receipts/'),
        ),
        migrations.AlterField(
            model_name='expensedetail',
            name='trip_detail',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='trips.tripdetail'),
        ),
        migrations.DeleteModel(
            name='DetailUser',
        ),
    ]
