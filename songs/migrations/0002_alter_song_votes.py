# Generated by Django 3.2 on 2021-07-09 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='votes',
            field=models.IntegerField(default=1),
        ),
    ]