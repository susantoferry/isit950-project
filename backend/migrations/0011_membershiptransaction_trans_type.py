# Generated by Django 4.1.7 on 2023-05-08 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_membershiptransaction_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='membershiptransaction',
            name='trans_type',
            field=models.CharField(max_length=1, null=True),
        ),
    ]