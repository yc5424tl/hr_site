from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.translation import gettext, gettext_lazy as _

# Register your models here.

class CustomUserAdmin(UserAdmin):
    # fieldsets = (
    #     (None, {'fields': ('username', 'password')}),
    #     (_('Personal Information'), {'fields': ('first_name', 'last_name', 'email', 'avatar')}),
    #     (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),}),
    #     (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),
    # )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('avatar',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('avatar',)})
    )

admin.site.register(User, CustomUserAdmin)