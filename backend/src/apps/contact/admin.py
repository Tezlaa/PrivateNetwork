from django.contrib import admin

from apps.contact.models import Contact


@admin.register(Contact)
class ContactAdminView(admin.ModelAdmin):
    def get_users(self, obj: Contact):
        return ', '.join([user.username for user in obj.connect.all()])
    
    list_display = ('id', 'get_users')
    get_users.short_description = 'Users'