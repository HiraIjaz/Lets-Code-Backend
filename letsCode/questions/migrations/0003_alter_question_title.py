# Generated by Django 4.2.5 on 2023-09-25 12:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("questions", "0002_rename_questions_question"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="title",
            field=models.TextField(help_text="title or description of the question"),
        ),
    ]
