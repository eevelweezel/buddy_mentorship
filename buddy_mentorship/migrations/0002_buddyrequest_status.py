# Generated by Django 3.0.3 on 2020-04-03 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("buddy_mentorship", "0001_squashed_0002_auto_20200228_0238"),
    ]

    operations = [
        migrations.AddField(
            model_name="buddyrequest",
            name="status",
            field=models.IntegerField(
                choices=[(0, "New"), (1, "Accepted"), (2, "Rejected")],
                default=0,
            ),
        ),
    ]