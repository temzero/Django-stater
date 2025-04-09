from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', _('Male')),
        ('F', _('Female')),
        ('O', _('Other')),
        ('P', _('Prefer not to say')),
    ]

    THEME_CHOICES = [
        ('light', _('Light')),
        ('dark', _('Dark')),
        ('system', _('System')),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name=_('Avatar')
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
        verbose_name=_('Gender')
    )
    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Birthday')
    )
    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Bio')
    )
    phone_number = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message=_("Enter a valid phone number.")
        )],
        verbose_name=_('Phone number')
    )
    theme = models.CharField(
        max_length=6,
        choices=THEME_CHOICES,
        default='system',
        null=True,
        blank=True,
        verbose_name=_('Theme')
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def avatarDisplay(self):
        try:
            return self.avatar.url
        except ValueError:
            return static('images/avatar.svg')

    @property
    def fullName(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
