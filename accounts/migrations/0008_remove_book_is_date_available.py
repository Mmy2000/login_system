# Generated by Django 4.2.7 on 2024-01-02 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_book_is_date_available'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='is_date_available',
        ),
    ]