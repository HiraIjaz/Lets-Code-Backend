# Generated by Django 4.2.5 on 2023-09-19 07:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("questions", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Questions",
            new_name="Question",
        ),
    ]
