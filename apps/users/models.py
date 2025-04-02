from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.core.validators import RegexValidator

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    ]
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('system', 'System Setting'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    phone_number = models.CharField(
        max_length=15, 
        null=True, 
        blank=True, 
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")]
    )
    theme = models.CharField(
        max_length=6, 
        choices=THEME_CHOICES, 
        default='light', 
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def avatarDisplay(self):
        try: avatar = self.avatar.url
        except: avatar = static('images/avatar.svg')
        return avatar
    
    @property
    def fullName(self):
        return f"{self.user.first_name} {self.user.last_name}"