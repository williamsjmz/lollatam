# Generated by Django 4.1.7 on 2023-03-19 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profile_country_alter_profile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.CharField(choices=[('AR', 'Argentina'), ('BO', 'Bolivia'), ('BZ', 'Belice'), ('CL', 'Chile'), ('CO', 'Colombia'), ('CR', 'Costa Rica'), ('CU', 'Cuba'), ('DM', 'Dominica'), ('DO', 'República Dominicana'), ('EC', 'Ecuador'), ('GU', 'Guatemala'), ('HN', 'Honduras'), ('HT', 'Haití'), ('JM', 'Jamaica'), ('MX', 'México'), ('NI', 'Nicaragua'), ('PA', 'Panamá'), ('PE', 'Perú'), ('PR', 'Puerto Rico'), ('PY', 'Paraguay'), ('SV', 'El Salvador'), ('UY', 'Uruguay'), ('VE', 'Venezuela')], max_length=2),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('H', 'Hombre'), ('M', 'Mujer'), ('O', 'Otro')], default='M', max_length=1),
        ),
    ]