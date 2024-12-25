# Generated by Django 5.1.4 on 2024-12-24 07:27

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('unique_key', models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True)),
            ],
        ),
    ]
