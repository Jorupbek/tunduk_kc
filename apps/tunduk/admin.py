from django.contrib import admin

from apps.tunduk.forms import CompanyForm
from apps.tunduk.models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_addr', 'client_id', 'member_code')
    list_display_links = ('name', 'ip_addr', 'client_id', 'member_code')
    search_fields = ['name', 'ip_addr', 'client_id', 'member_code']
    form = CompanyForm
