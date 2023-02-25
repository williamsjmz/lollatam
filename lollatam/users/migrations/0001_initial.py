# Generated by Django 4.1.7 on 2023-02-25 23:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=15)),
                ('country', models.CharField(choices=[('AR', 'Argentina'), ('BO', 'Bolivia'), ('BZ', 'Belice'), ('CL', 'Chile'), ('CO', 'Colombia'), ('CR', 'Costa Rica'), ('CU', 'Cuba'), ('DM', 'Dominica'), ('DO', 'República Dominicana'), ('EC', 'Ecuador'), ('GU', 'Guatemala'), ('HN', 'Honduras'), ('HT', 'Haití'), ('JM', 'Jamaica'), ('MX', 'México'), ('NI', 'Nicaragua'), ('PA', 'Panamá'), ('PE', 'Perú'), ('PR', 'Puerto Rico'), ('PY', 'Paraguay'), ('SV', 'El Salvador'), ('UY', 'Uruguay'), ('VE', 'Venezuela')], max_length=2)),
                ('desciption', models.TextField(blank=True, max_length=150, null=True)),
                ('gender', models.CharField(choices=[('F', 'Hombre'), ('M', 'Mujer'), ('O', 'Otro')], default='M', max_length=1)),
                ('image', models.ImageField(blank=True, default='profile-pictures/default-user-pp.png', null=True, upload_to='profile-pictures')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('server', models.CharField(choices=[('LAN', 'Latinoamérica Norte'), ('LAS', 'Latinoamérica Sur')], max_length=3)),
                ('profile', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='users.profile')),
            ],
        ),
    ]
