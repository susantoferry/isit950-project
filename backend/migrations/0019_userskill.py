# Generated by Django 4.1.7 on 2023-04-11 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0018_merge_20230409_1230'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.skill')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
