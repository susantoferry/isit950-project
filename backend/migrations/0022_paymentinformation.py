# Generated by Django 4.1.7 on 2023-04-18 07:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0021_alter_userskill_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_card', models.CharField(max_length=16)),
                ('expiry_date', models.DateField()),
                ('cvv', models.CharField(max_length=3)),
                ('create_date', models.DateTimeField(null=True)),
                ('modify_date', models.DateTimeField(null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_paymentinfo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]