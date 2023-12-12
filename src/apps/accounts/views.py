from typing import Any

from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import FormView


class SingUp(FormView):
    template_name = 'registration/singUp.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('lobbies')
    
    def form_valid(self, form: Any) -> HttpResponse:
        user = form.save()
        auth_login(self.request, user)
        return redirect(self.get_success_url())