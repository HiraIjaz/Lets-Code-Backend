# Generated by Django 4.2.5 on 2023-09-27 07:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("questions", "0004_remove_question_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="isDeleted",
            field=models.BooleanField(default=False),
        ),
    ]
