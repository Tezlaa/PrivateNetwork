from django.contrib import admin

from apps.lobby.models import Lobby


@admin.register(Lobby)
class LobbyAdminView(admin.ModelAdmin):
    def user_connected_display(self, obj) -> str:
        return str(obj.user_connected.count())

    def messages(self, obj) -> str:
        return str(obj.chat.count())
    
    list_display = ('lobby_name', 'password', 'user_limit', 'user_connected_display', 'messages')
    user_connected_display.short_description = 'User connect'
    messages.short_description = 'Message count'