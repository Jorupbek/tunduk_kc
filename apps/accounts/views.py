from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy

from apps.accounts.models import CustomUser


class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('tunduk:tunduk-controller')

    def form_valid(self, form):
        super().form_valid(form)

        messages.success(self.request, 'Ващ пароль успешно  изменени.')

        return super().form_valid(form)


def reset_password_view(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
        user.set_password("Password123")
        user.save()
        messages.success(
            request,
            f"Пароль для пользователя {user.username} успешно обновлен. на `Password123`"
        )
        return redirect('admin:accounts_customuser_changelist')
    except Exception as e:
        messages.error(
            request,
            f"Ошибка при сбросе пароля {e}"
        )
        return redirect(
            'admin:accounts_customuser_changelist'
        )
