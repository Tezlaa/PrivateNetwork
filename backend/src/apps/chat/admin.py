from django.contrib import admin

from apps.chat.models import FileMessage, Message


@admin.register(Message)
class MessageAdminView(admin.ModelAdmin):
    def user_liked_display(self, obj) -> str:
        return str(obj.user_liked.count())
    
    list_display = ('user', 'message', 'reply_message', 'user_liked_display', 'created_at')
    user_liked_display.short_description = 'Likes'
    

@admin.register(FileMessage)
class FileAdminView(admin.ModelAdmin):
    list_display = ('id', 'sign', 'file')
    list_editable = ('sign', )