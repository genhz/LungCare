# Generated by Django 3.2 on 2023-04-05 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_auto_20230405_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='img',
            name='img',
            field=models.ImageField(default='暂无', upload_to='img'),
        ),
        migrations.AlterField(
            model_name='img',
            name='name',
            field=models.CharField(default='暂无', max_length=100),
        ),
    ]