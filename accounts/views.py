from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden

from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import CustomUser
from .forms import CustomUserChangeForm

from django.db.models import Q

from .models import RelationRequest, Relation
from .forms import RelationRequestForm, RelationAcceptForm, RelationRequestUndoForm, RelationDeleteForm



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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_id = self.kwargs['pk']
        context['account'] = CustomUser.objects.get(id=account_id) #making sure that the profile we use in the context (to be shown) is only the profile the user making the request

        search = self.request.GET.get('search-area') or ''
        if search is not None:
            context['searched_users'] = CustomUser.objects.exclude(id=account_id).filter(Q(email__icontains = search) | Q(first_name__icontains = search) | Q(last_name__icontains = search) )

        context['search_input'] = search

        # retrieving the Relation objects if logged user in the Relation object (either as sender or receiver)
        relations = Relation.objects.filter(Q(user_sending__exact=self.request.user.id)|Q(user_receiving__exact=self.request.user.id))
        context['relations'] = relations

        relations_users = CustomUser.objects.filter(Q(relation_receiver__in = relations)|Q(relation_sender__in = relations)).exclude(id=account_id)
        context['relations_users'] = relations_users

        context['relation_request_form'] = RelationRequestForm()
        context['accept_form'] = RelationAcceptForm()
        context['undo_request_form'] = RelationRequestUndoForm()


        context['friendship_exists'] = (Relation.objects.filter(user_sending_id=self.request.user.id, user_receiving_id=account_id).exists() or Relation.objects.filter(user_sending_id=account_id, user_receiving_id=self.request.user.id).exists())
        context['request_from_exists'] = RelationRequest.objects.filter(user_sending_id=account_id, user_receiving=self.request.user.id).exists()
        context['request_to_exists'] = RelationRequest.objects.filter(user_sending_id=self.request.user.id, user_receiving=account_id).exists()



        return context

    def post(self, request, *args, **kwargs):
        account_id = self.kwargs['pk']

        if "request_form" in request.POST:
            request_form = RelationRequestForm(request.POST)
            if request_form.is_valid():
                sender = self.request.user
                receiver = CustomUser.objects.get(id=account_id)

                RelationRequest.objects.create(
                    user_receiving=receiver,
                    user_sending=sender,
                )

        elif "accept_form" in request.POST:
            accept_form = RelationAcceptForm(request.POST)
            if accept_form.is_valid():
                sender = CustomUser.objects.get(id=account_id)
                receiver = self.request.user
                relation_type = accept_form.cleaned_data['relation_type']

                request_to_delete = RelationRequest.objects.get(
                    user_receiving=receiver,
                    user_sending=sender,
                )
                request_to_delete.delete()

                Relation.objects.create(
                    user_receiving = receiver,
                    user_sending = sender,
                    relation_type=relation_type,
                )

        elif "undo_request_form" in request.POST:
            undo_request_form = RelationRequestUndoForm(request.POST)
            if undo_request_form.is_valid():
                sender = self.request.user
                receiver = CustomUser.objects.get(id=account_id)

                request_to_delete = RelationRequest.objects.get(
                    user_receiving=receiver,
                    user_sending=sender,
                )
                request_to_delete.delete()

        elif "delete_form" in request.POST:
            delete_form = RelationDeleteForm(request.POST)
            if delete_form.is_valid():
                sender = self.request.user
                receiver = CustomUser.objects.get(id=account_id)

            request_to_delete = Relation.objects.filter(
                Q(user_receiving=receiver,user_sending=sender) | Q(user_receiving=sender, user_sending=receiver))
            request_to_delete.first().delete()

        return redirect('accounts:account_view', pk=account_id)
