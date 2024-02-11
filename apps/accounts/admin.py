from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['id', 'username', 'first_name', 'last_name', 'company',]
    list_display_links = ['id', 'username', 'first_name', 'last_name', 'company',]
    list_filter = "company",
    fieldsets = (
        (None, {"fields": ("username", "password", "company")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                )
            }
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_admin",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    actions = ['reset_password']

    def reset_password(self, request, queryset):
        for user in queryset:
            user.set_password('Password123')
            user.save()
            self.message_user(
                request,
                f"Пароль для пользователя {user.username} успешно обновлен.",
                messages.SUCCESS
            )

    def reset_password_button(self, obj):
        reset_password_url = reverse('reset_password', args=[obj.pk])
        return format_html('<a class="button" href="/upr/admin/accounts/reset-password/{}/">Reset Password</a>', obj.pk)

    def get_list_display(self, request):
        return super().get_list_display(request) + ['reset_password_button']

    reset_password_button.short_description = "Сброс пароля"
    reset_password.short_description = "Сброс пароля"

