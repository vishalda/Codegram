# Generated by Django 4.1.1 on 2022-09-09 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
        ('post', '0002_pullrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='GroupId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='group.group'),
        ),
    ]
