from django.contrib import admin

from .models import ChangeLog, TundukRequestLog


@admin.register(ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'action_on_model', 'model', 'user', 'changed',)
    list_display_links = ('record_id', 'action_on_model', 'model', 'user', 'changed',)
    readonly_fields = ('user',)
    list_filter = ('model', 'action_on_model',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return request.user.is_superuser


@admin.register(TundukRequestLog)
class TundukRequestLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'request_type')
    list_display_links = ('id', 'user', 'created_at', 'request_type')
    readonly_fields = ('user', 'request_type')
    list_filter = ('user', 'request_type')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return request.user.is_superuser

    def user_company(self, obj):
        return obj.user.company

    user_company.short_description = 'КС пользователя'
