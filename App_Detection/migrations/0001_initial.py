# Generated by Django 5.0.2 on 2024-02-17 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestMedia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.ImageField(blank=True, upload_to='uploaded_files')),
            ],
        ),
    ]
