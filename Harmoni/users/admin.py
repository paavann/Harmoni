from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import User



class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'is_active', 'is_staff', 'is_superuser')

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'is_active', 'is_staff', 'is_superuser')

class UserAdmin(BaseUserAdmin):
    model = User
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ('email', 'name', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

admin.site.register(User, UserAdmin)