# Generated by Django 2.0.4 on 2018-08-21 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20180821_1712'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back', 'book'], 'permissions': (('can_mark_returned', 'Set book as returned'), ('can_renew', 'Renew book due date'))},
        ),
    ]