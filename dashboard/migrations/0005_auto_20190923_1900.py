# Generated by Django 2.2.4 on 2019-09-23 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20190917_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tissuesensor',
            name='empty_reading',
            field=models.CharField(default='8', max_length=255),
        ),
    ]
