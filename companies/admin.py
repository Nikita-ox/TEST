from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Company, Product
from .tasks import async_clear_debt


@admin.action(description='Очиcтить задолженность перед поставщиком')
def clear_debt(modeladmin, request, queryset):
    if len(queryset) > 20:
        async_clear_debt.delay(list(queryset.values('id')))
        return
    queryset.update(debt=0)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('hierarchy', 'name', 'country',
                    'city', 'provider_link', 'debt')
    list_display_links = ('name', )
    list_filter = ('city', 'hierarchy')
    actions = [clear_debt]

    def provider_link(self, obj):

        if obj.provider:
            link = reverse(
                'admin:companies_company_change',
                args=(obj.provider.id,)
            )
            return mark_safe(
                u"<a href='{0}'>{1}</a>".format(link, obj.provider)
            )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'release_date')
    list_filter = ('name',)
