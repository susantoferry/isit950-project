# Generated by Django 4.2.1 on 2023-05-20 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0017_transaction_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='offer',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
