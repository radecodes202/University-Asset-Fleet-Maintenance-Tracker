from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ('email', 'get_full_name', 'employee_id', 'department', 'role', 'is_active')
    list_filter   = ('role', 'is_active', 'department')
    search_fields = ('email', 'first_name', 'last_name', 'employee_id')
    ordering      = ('last_name', 'first_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'employee_id', 'department')}),
        ('Role & Access', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'employee_id', 'department', 'role', 'password1', 'password2'),
        }),
    )