from django.contrib import admin

from apps.accounts.models import User


@admin.register(User)
class AdminUserView(admin.ModelAdmin):
    list_display = ('id', 'username', 'date_joined', 'avatar')