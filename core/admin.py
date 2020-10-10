from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'office', 'is_staff')
    list_filter = ('is_staff', 'is_superuser')

# admin.site.register(User)
admin.site.register(Office)
admin.site.register(PurchaseProduct)
admin.site.register(Stock)
admin.site.register(SellProduct)