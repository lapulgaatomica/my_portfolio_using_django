# Generated by Django 3.1.7 on 2021-02-21 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='paragraph',
            field=models.TextField(max_length=400),
        ),
    ]
