# Generated by Django 2.2.4 on 2019-09-16 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smellsensor',
            name='level_smellsensor',
            field=models.CharField(blank=True, default='0.50', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='soapsensor',
            name='level_soapsensor',
            field=models.CharField(default='4', max_length=255),
        ),
        migrations.AlterField(
            model_name='tissuesensor',
            name='level_tissuesensor',
            field=models.CharField(blank=True, default='3', max_length=255, null=True),
        ),
    ]
