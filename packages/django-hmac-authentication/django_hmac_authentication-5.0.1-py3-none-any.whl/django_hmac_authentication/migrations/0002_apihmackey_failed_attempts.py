# Generated by Django 4.1.7 on 2023-05-31 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_hmac_authentication", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="apihmackey",
            name="failed_attempts",
            field=models.PositiveSmallIntegerField(
                default=0, verbose_name="Failed authentication attempts"
            ),
        ),
    ]
