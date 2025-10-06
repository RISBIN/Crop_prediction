from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin."""

    list_display = ('username', 'email', 'user_type', 'location', 'state', 'is_staff', 'date_joined')
    list_filter = ('user_type', 'is_staff', 'is_active', 'state')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'location')

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'location', 'state', 'country', 'farm_size')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'location', 'state', 'country', 'farm_size')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """User Profile Admin."""

    list_display = ('user', 'preferred_language', 'email_notifications', 'sms_notifications')
    list_filter = ('preferred_language', 'email_notifications', 'sms_notifications')
    search_fields = ('user__username', 'user__email')
