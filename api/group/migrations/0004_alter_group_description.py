# Generated by Django 4.1.1 on 2022-09-19 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0003_group_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='Description',
            field=models.TextField(blank=True, null=True),
        ),
    ]