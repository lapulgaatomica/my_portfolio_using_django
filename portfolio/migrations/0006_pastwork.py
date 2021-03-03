# Generated by Django 3.1.7 on 2021-03-03 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='PastWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(max_length=75)),
                ('github_link', models.URLField(max_length=100, unique=True)),
                ('page_link', models.URLField(blank=True, max_length=100, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
