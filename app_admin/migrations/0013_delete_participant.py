# Generated by Django 5.2.3 on 2025-07-05 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_admin', '0012_alter_category_category_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Participant',
        ),
    ]
