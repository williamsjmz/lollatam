from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    '''
    Model that represents a user in the database
    '''
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    username = models.CharField(max_length=50, null=False, blank=False, unique=True)
    email = models.EmailField(null=False, blank=False, unique=True)
    password1 = models.CharField(max_length=25)
    password2 = models.CharField(max_length=25)
    birthday = models.DateField(null=False, blank=False)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name}: {self.email}'

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

    def __str__(self):
        return f'{self.username}'

class Account(models.Model):
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