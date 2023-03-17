from django.db import models
from django.contrib.auth.models import User

# Make email field unique for the User model.
User._meta.get_field('email')._unique = True

class Profile(models.Model):
    '''
    Model that represents a user profile in the databaseS
    '''
    COUNTRIES = [
        ('AR', 'Argentina'),
        ('BO', 'Bolivia'),
        ('BZ', 'Belice'),
        ('CL', 'Chile'),
        ('CO', 'Colombia'),
        ('CR', 'Costa Rica'),
        ('CU', 'Cuba'),
        ('DM', 'Dominica'),
        ('DO', 'República Dominicana'),
        ('EC', 'Ecuador'),
        ('GU', 'Guatemala'),
        ('HN', 'Honduras'),
        ('HT', 'Haití'),
        ('JM', 'Jamaica'),
        ('MX', 'México'),
        ('NI', 'Nicaragua'),
        ('PA', 'Panamá'),
        ('PE', 'Perú'),
        ('PR', 'Puerto Rico'),
        ('PY', 'Paraguay'),
        ('SV', 'El Salvador'),
        ('UY', 'Uruguay'),
        ('VE', 'Venezuela'),
    ]

    GENDERS = [
        ('F', 'Hombre'),
        ('M', 'Mujer'),
        ('O', 'Otro'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", null=False, blank=False)
    username = models.CharField(max_length=15, null=False, blank=False)
    country = models.CharField(max_length=2, choices=COUNTRIES, null=False, blank=False)
    desciption = models.TextField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=1, null=False, blank=False, choices=GENDERS, default='M')
    image = models.ImageField(upload_to='profile-pictures', default='profile-pictures/default-user-pp.png', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Fields added for email verification functionality.
    verification_token = models.CharField(max_length=64, null=True, blank=True)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username}'

class GameAccount(models.Model):
    '''
    Model that represents a game account in the database
    '''
    SERVERS = [
        ('LAN', 'Latinoamérica Norte'),
        ('LAS', 'Latinoamérica Sur'),
    ]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, related_name='accounts')
    username = models.CharField(max_length=100, null=False, blank=False)
    server = models.CharField(max_length=3, choices=SERVERS, null=False, blank=False)

    def __str__(self):
        return f'{self.username}'