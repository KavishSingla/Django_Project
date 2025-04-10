from django.contrib import admin
from .models import CreditCard, UserCardApplication

@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(UserCardApplication)
class UserCardApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'credit_card', 'applied_on')
    search_fields = ('user__email',)
    list_filter = ('credit_card',)
