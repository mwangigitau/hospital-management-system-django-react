from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role, Permission, AuditLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'employee_id', 'role', 'is_active')
    list_filter = ('is_active', 'is_staff', 'role', 'department')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'employee_id')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('HMS Info', {'fields': ('employee_id', 'phone', 'department', 'branch', 'role', 'profile_picture')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('HMS Info', {'fields': ('employee_id', 'phone', 'department', 'branch', 'role')}),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    filter_horizontal = ('permissions',)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'codename', 'module')
    list_filter = ('module',)
    search_fields = ('name', 'codename')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model_name', 'object_id', 'ip_address', 'timestamp')
    list_filter = ('action', 'model_name')
    search_fields = ('user__username', 'model_name', 'object_id')
    readonly_fields = ('user', 'action', 'model_name', 'object_id', 'changes', 'ip_address', 'timestamp')
