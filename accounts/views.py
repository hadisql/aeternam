from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden

from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import CustomUser
from .forms import CustomUserChangeForm


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    context_object_name = 'account'
    template_name = 'accounts/account_update.html'

    def test_func(self):
        account_id = self.kwargs['pk']
        account = CustomUser.objects.get(id=account_id)
        return self.request.user == account  # Check if the profile-update page is accessed by the same logged user

    def handle_no_permission(self):
        return HttpResponseForbidden("You don't have permission to update this profile.")

    def get_success_url(self):
        # cannot use reverse_lazy with pk to get back to user's profile
        return reverse('accounts:account_view', kwargs={'pk':self.kwargs['pk']})

class UserView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'accounts/account.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_id = self.kwargs['pk']
        context['account'] = CustomUser.objects.get(id=account_id) #making sure that the profile we use in the context (to be shown) is only the profile the user making the request

        return context
