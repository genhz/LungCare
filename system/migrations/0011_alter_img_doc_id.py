# Generated by Django 3.2 on 2023-04-13 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0010_dr_describe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='img',
            name='doc_id',
            field=models.CharField(default='未预约', max_length=20),
        ),
    ]