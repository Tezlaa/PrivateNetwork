from typing import Any
from django.views.generic import TemplateView


from apps.lobby.models import Lobby
from apps.chat.services.model_services import create_like_for_message


class ChatView(TemplateView):
    template_name = 'chat/index.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        lobby = Lobby.objects.filter(pk=7)[0]
        print(create_like_for_message(lobby, 3, 'root'))
        
        return super().get_context_data(**kwargs)