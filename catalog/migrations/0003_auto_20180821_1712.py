# Generated by Django 2.0.4 on 2018-08-21 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_bookinstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back', 'book'], 'permissions': (('can_mark_returned', 'Set book as returned'),)},
        ),
    ]
