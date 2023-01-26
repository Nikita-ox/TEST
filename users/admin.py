from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'first_name',
                    'last_name', 'email', 'company_link')
    list_display_links = ('username', )
    list_filter = ('company',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1',
                       'password2', 'first_name',
                       'last_name', 'email', 'company',
                       'is_staff', 'is_active')}),
    )

    def company_link(self, obj):

        if obj.company:
            link = reverse(
                'admin:companies_company_change',
                args=(obj.company.id,)
            )
            return mark_safe(
                u"<a href='{0}'>{1}</a>".format(link, obj.company)
            )
