# Generated by Django 5.2.3 on 2025-06-16 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0005_alter_event_age"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="event_id",
        ),
        migrations.AlterField(
            model_name="event",
            name="title",
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
