# Generated by Django 4.1.7 on 2023-04-14 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0025_alter_profile_membership'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='img_profile',
            field=models.ImageField(blank=True, null=True, upload_to='images/profiles'),
        ),
    ]
