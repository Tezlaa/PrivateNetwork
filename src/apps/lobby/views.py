from django.views.generic import TemplateView


class LobbyMenu(TemplateView):
    template_name = 'lobby/index.html'