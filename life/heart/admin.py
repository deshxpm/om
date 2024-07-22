from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email','password')
    list_filter = ('email', 'phone')
    search_fields = ('email', 'phone')
    readonly_fields = ('password',)

admin.site.register(UserProfile,UserProfileAdmin)