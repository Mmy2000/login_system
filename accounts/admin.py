from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account , Profile , Day , Book

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active','is_admin')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
admin.site.register(Profile)
class DayAdmin(admin.ModelAdmin):
    list_display = ( 'day' ,'user', 'date' , 'is_booked')
admin.site.register(Day)
admin.site.register(Book,DayAdmin)