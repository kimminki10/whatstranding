# Generated by Django 5.1.3 on 2024-11-12 13:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
        ('trends', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trend',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.post'),
        ),
    ]
