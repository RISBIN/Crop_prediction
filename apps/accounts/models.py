from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from config.supabase_storage import ProfilePictureStorage


class CustomUser(AbstractUser):
    """Extended User model with additional fields."""

    USER_TYPE_CHOICES = [
        ('farmer', 'Farmer'),
        ('researcher', 'Researcher'),
        ('admin', 'Administrator'),
    ]

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='farmer',
        verbose_name=_('User Type')
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_('Phone Number')
    )

    location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Location')
    )

    state = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_('State')
    )

    country = models.CharField(
        max_length=50,
        default='India',
        verbose_name=_('Country')
    )

    farm_size = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('Farm size in acres'),
        verbose_name=_('Farm Size (acres)')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class UserProfile(models.Model):
    """Additional profile information for users."""

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Biography')
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        storage=ProfilePictureStorage(),
        blank=True,
        null=True,
        verbose_name=_('Profile Picture')
    )

    preferred_language = models.CharField(
        max_length=10,
        default='en',
        choices=[
            ('en', 'English'),
            ('hi', 'Hindi'),
            ('ta', 'Tamil'),
            ('te', 'Telugu'),
        ],
        verbose_name=_('Preferred Language')
    )

    email_notifications = models.BooleanField(
        default=True,
        verbose_name=_('Email Notifications')
    )

    sms_notifications = models.BooleanField(
        default=False,
        verbose_name=_('SMS Notifications')
    )

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

    def __str__(self):
        return f"Profile of {self.user.username}"
