# Generated by Django 4.2.7 on 2024-01-02 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
