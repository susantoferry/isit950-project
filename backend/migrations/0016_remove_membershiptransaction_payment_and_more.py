# Generated by Django 4.1.7 on 2023-05-13 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0015_task_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membershiptransaction',
            name='payment',
        ),
        migrations.AddField(
            model_name='membershiptransaction',
            name='credit_card',
            field=models.CharField(max_length=255, null=True),
        ),
    ]