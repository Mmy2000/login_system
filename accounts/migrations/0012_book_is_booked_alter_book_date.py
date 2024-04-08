# Generated by Django 4.2.7 on 2024-04-08 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_book_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_booked',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='date',
            field=models.IntegerField(choices=[(2, 'الساعه 2'), (3, 'الساعه 3'), (4, '4 الساعه'), (5, '5 الساعه'), (6, '6 الساعه'), (7, '7 الساعه'), (8, '8 الساعه'), (9, '9 الساعه'), (10, '10 الساعه'), (11, '11 الساعه'), (12, '12 الساعه')]),
        ),
    ]
