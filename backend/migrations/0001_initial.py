# Generated by Django 4.2.1 on 2023-05-21 04:40

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('img_profile', models.CharField(blank=True, max_length=100, null=True)),
                ('img_background', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('unit', models.CharField(blank=True, default='-', max_length=10, null=True)),
                ('city', models.CharField(blank=True, max_length=30, null=True)),
                ('state', models.CharField(blank=True, max_length=20, null=True)),
                ('zip', models.CharField(blank=True, max_length=10, null=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=3, null=True)),
                ('email_verified', models.BooleanField(default=0, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('create_date', models.DateTimeField(null=True)),
                ('modify_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('booking_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('location', models.TextField(null=True)),
                ('location_link', models.CharField(blank=True, max_length=100, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('long', models.FloatField(blank=True, null=True)),
                ('completed_on', models.DateField()),
                ('status', models.IntegerField(default=0)),
                ('is_paid', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('modify_date', models.DateTimeField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='backend.category')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_client', related_query_name='profile', to=settings.AUTH_USER_MODEL)),
                ('user_provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_provider', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_bookmark', to='backend.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_bookmark', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=0, default=0, max_digits=12, null=True)),
                ('admin_fee', models.DecimalField(decimal_places=0, default=0, max_digits=12, null=True)),
                ('total_price', models.DecimalField(decimal_places=0, default=0, max_digits=12, null=True)),
                ('is_payee', models.BooleanField(default=0, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_trans', to='backend.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_trans', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_sp', models.TextField(blank=True, null=True)),
                ('comment_client', models.TextField(blank=True, null=True)),
                ('rating_sp', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=3, null=True)),
                ('rating_client', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=3, null=True)),
                ('create_date', models.DateTimeField(null=True)),
                ('modify_date', models.DateTimeField(null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_review', to='backend.task')),
                ('user_client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rev_user_client', to=settings.AUTH_USER_MODEL)),
                ('user_sp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rev_user_sp', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('parent_id', models.IntegerField(null=True)),
                ('create_date', models.DateTimeField(null=True)),
                ('modify_date', models.DateTimeField(null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_task_id', to='backend.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_user_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=0, default=0, max_digits=6)),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='category_price', to='backend.category')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_card', models.CharField(max_length=255)),
                ('expiry_date', models.CharField(max_length=255)),
                ('cvv', models.CharField(max_length=255)),
                ('create_date', models.DateTimeField(null=True)),
                ('modify_date', models.DateTimeField(null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_paymentinfo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PasswordToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=60)),
                ('status', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('modify_date', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userToken', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, null=True)),
                ('admin_fee', models.DecimalField(decimal_places=2, max_digits=7, null=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=7, null=True)),
                ('description', models.TextField()),
                ('create_date', models.DateTimeField(null=True)),
                ('modify_date', models.DateTimeField(null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_task_id', to='backend.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_sp_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_notif', models.IntegerField(null=True)),
                ('is_read', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(null=True)),
                ('modify_date', models.DateTimeField(null=True)),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_notification', to='backend.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_notif', to=settings.AUTH_USER_MODEL)),
                ('user_sp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_sp', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MembershipTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership', models.IntegerField()),
                ('trans_type', models.CharField(max_length=1, null=True)),
                ('credit_card', models.CharField(max_length=255, null=True)),
                ('price', models.DecimalField(decimal_places=0, default=0, max_digits=4)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trans_user_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
