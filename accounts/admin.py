from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser,Profile

class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'first_name', 'last_name','username', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','username','Messsage_preview','profile_picture')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','email_verified')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name','profile_picture', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name')
    readonly_fields = ('date_joined',)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Profile)
