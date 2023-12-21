from django.contrib import admin

from apps.chat.models import Message


@admin.register(Message)
class MessageAdminView(admin.ModelAdmin):
    def user_liked_display(self, obj) -> str:
        return str(obj.user_liked.count())
    
    list_display = ('user', 'message', 'user_liked_display', 'created_at')
    user_liked_display.short_description = 'Likes'