from django.contrib import admin

from apps.accounts.models import User


@admin.register(User)
class AdminUserView(admin.ModelAdmin):
    def get_contacts(self, obj: User) -> str:
        return str(obj.contacts.count())
    
    list_display = ('id', 'username', 'date_joined', 'avatar', 'get_contacts')
    get_contacts.short_description = 'Contacts count'