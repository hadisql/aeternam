from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string

from django.views.generic import FormView, UpdateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .models import CustomUser
from .forms import CustomUserChangeForm, CustomPasswordChangeForm

from django.db.models import Q

from .models import RelationRequest, Relation, Notification
from .forms import RelationRequestForm, RelationAcceptForm, RelationRequestUndoForm, RelationDeleteForm, RegisterForm, RelationChangeForm
from .models import create_notification
from django.contrib.contenttypes.models import ContentType

from photos.models import Photo
from comments_likes.models import Comment

from django.contrib import messages #used in NotificationsView
from django.utils.translation import gettext_lazy as _

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import send_mail

from aeternam.settings import EMAIL_HOST_USER

class RegisterPage(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    redirect_authenticated_user = True # we want to redirect authenticated users if trying to access the register page -> doesn't seem to work
    success_url = reverse_lazy('albums:albums_view')

    def form_valid(self, form):
        print('FORM IS VALID')
        user = form.save(commit=False)
        user.is_active = False  # User is not active until they click the activation link
        user.save()

        # Send activation email
        self.send_activation_email(user)
        print('send_activation_email FUNCTION TRIGGERED IN VIEWS')

        # Display a message to the user
        messages.success(
            self.request,
            _("Please check your email to activate your account.")
        )

        return super(RegisterPage, self).form_valid(form)

    def send_activation_email(self, user):
        current_site = get_current_site(self.request)
        subject = _('Aeternam - Activate Your Account')
        message = render_to_string('accounts/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        from_email = EMAIL_HOST_USER
        to_email = user.email
        send_mail(subject, message, from_email, [to_email])

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('albums:albums_view') #forces to redirect to main page when user is authenticated
        return super(RegisterPage, self).get(*args, **kwargs) #otherwise we apply the original method


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, _('Your account has been activated!'))
        return redirect('albums:albums_view')
    else:
        return HttpResponse(_('Activation link is invalid or expired.'))

def loginpage(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Use eamail to authenticate instead of username
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('albums:albums_view'))
        else:
            # Check for the specific reason for authentication failure
            try:
                user = CustomUser.objects.get(email=email)
                if not user.check_password(password):
                    # Password is incorrect
                    messages.error(request, _('Incorrect password. Please try again.'))
                else:
                    # User exists, but some other issue (should not reach here in normal cases)
                    messages.error(request, _('Authentication failed. Please try again.'))
            except CustomUser.DoesNotExist:
                # User with the given email does not exist
                messages.error(request, _('User with this email does not exist.'))

            return render(request, 'accounts/login.html')
    else:
        return render(request, 'accounts/login.html')


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

    def form_valid(self, form):
        print(form.changed_data)
        print("self.request.post", self.request.POST)
        return super().form_valid(form)

class ChangePasswordView(LoginRequiredMixin, View):
    template_name = 'accounts/change_password.html'
    form_class = CustomPasswordChangeForm  # Use the custom form class you created

    def get(self, request, *args, **kwargs):
        form = self.form_class(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(
                self.request,
                _("Your password has been changed successfully")
            )
            return redirect('accounts:edit_account', pk=request.user.pk)
        return render(request, self.template_name, {'form': form})


def user_search(request):
    context = {}
    url_parameter = request.GET.get("q")

    relations = Relation.objects.filter(Q(user_sending__exact=request.user.id)
                                        |Q(user_receiving__exact=request.user.id))
    context['relations'] = relations # all relations with user

    relations_users = CustomUser.objects.filter(Q(relation_receiver__in = relations)|Q(relation_sender__in = relations)).exclude(id=request.user.id)
    context['relations_users'] = relations_users # all users in relation with user

    if url_parameter:
        searched_users = CustomUser.objects.exclude(id=request.user.id).filter(Q(email__icontains = url_parameter) | Q(first_name__icontains = url_parameter) | Q(last_name__icontains = url_parameter) )
        searched_users = searched_users.exclude(id__in=relations_users) # we exclude users already related from research
        if not searched_users:
            #if no user is found
            searched_users = "No results"
    else:
        searched_users = url_parameter #None

    context['searched_users'] = searched_users

    does_req_accept_json = request.accepts("application/json")
    is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest" and does_req_accept_json
    if is_ajax_request:
        html = render_to_string(
            template_name="partials/searchbar_results.html",
            context=context
        )
        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    return render(request, "accounts/account.html", context=context)

class UserView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'accounts/account.html'

    def exclude_logged_user(self, user_qlist):
        '''excludes logged user from queryset'''
        return user_qlist.exclude(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_id = self.kwargs['pk']
        context['account'] = CustomUser.objects.get(id=account_id) #making sure that the profile we use in the context (to be shown) is the profile visited

        # search = self.request.GET.get('search-area') or ''
        # if search is not None:
        #     context['searched_users'] = CustomUser.objects.exclude(id=account_id).filter(Q(email__icontains = search) | Q(first_name__icontains = search) | Q(last_name__icontains = search) )

        # context['search_input'] = search

        # retrieving the Relation objects if logged user in the Relation object (either as sender or receiver)
        relations = Relation.objects.filter(Q(user_sending__exact=account_id)
                                            |Q(user_receiving__exact=account_id))
        context['relations'] = relations # all relations with user

        relations_users = CustomUser.objects.filter(Q(relation_receiver__in = relations)|Q(relation_sender__in = relations)).exclude(id=account_id)
        context['relations_users'] = relations_users # all users in relation with user

        other_user_in_relations = [(relation.user_sending if relation.user_sending.id != account_id else relation.user_receiving) for relation in relations] # for each relation object, list the user not logged ('other user')
        context['users_relations_dict'] = {key:value for key,value in zip(other_user_in_relations, relations) }

        context['relation_request_form'] = RelationRequestForm()
        context['accept_form'] = RelationAcceptForm()
        context['undo_request_form'] = RelationRequestUndoForm()
        context['relation_change_form'] = RelationChangeForm()


        context['relation_exists'] = self.request.user in relations_users # True if visisted account is connected to logged user
        context['request_from_exists'] = RelationRequest.objects.filter(user_sending_id=account_id, user_receiving=self.request.user.id).exists()
        context['request_to_exists'] = RelationRequest.objects.filter(user_sending_id=self.request.user.id, user_receiving=account_id).exists()

        # retrieving user data for profile dashboard
        context['account_photos'] = Photo.objects.filter(uploaded_by=account_id)
        context['account_comments'] = Comment.objects.filter(author=account_id)

        context['relation_to_change'] = Relation.objects.filter(
                    Q(user_receiving=account_id, user_sending=self.request.user)|
                    Q(user_receiving=self.request.user, user_sending=account_id)).first() #only 1 relation is filtered here

        return context

    def post(self, request, *args, **kwargs):
        account_id = self.kwargs['pk']
        account_id_user = CustomUser.objects.get(id=account_id)

        if "request_form" in request.POST:
            request_form = RelationRequestForm(request.POST)
            if request_form.is_valid():
                sender = self.request.user
                receiver = account_id_user

                RelationRequest.objects.create(
                    user_receiving=receiver,
                    user_sending=sender,
                )

        elif "accept_form" in request.POST:
            accept_form = RelationAcceptForm(request.POST)
            if accept_form.is_valid():
                sender = account_id_user
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
                print(f"last relation object : {Relation.objects.last()}\nwith ID : {Relation.objects.last().pk}")
                # notify the user that the request was accepted :
                title = _("Connection created")
                message = _("{} has accepted your connection request").format(self.request.user.get_full_name())
                create_notification(user=account_id_user, user_from=self.request.user, content_type=ContentType.objects.get_for_model(Relation), object_id=Relation.objects.last().pk, message=message, title=title)

        elif "undo_request_form" in request.POST:
            undo_request_form = RelationRequestUndoForm(request.POST)
            if undo_request_form.is_valid():
                sender = self.request.user
                receiver = account_id_user

                request_to_delete = RelationRequest.objects.get(
                    user_receiving=receiver,
                    user_sending=sender,
                )
                request_to_delete.delete()

        elif "delete_form" in request.POST:
            delete_form = RelationDeleteForm(request.POST)
            if delete_form.is_valid():
                sender = self.request.user
                receiver = account_id_user

            request_to_delete = Relation.objects.filter(
                Q(user_receiving=receiver,user_sending=sender) | Q(user_receiving=sender, user_sending=receiver))
            request_to_delete.first().delete()

        elif "relation_change_form" in request.POST:
            relation_change_form = RelationChangeForm(request.POST)

            if relation_change_form.is_valid():
                new_relation_type = relation_change_form.cleaned_data['change_relation']

                relation_to_change = Relation.objects.filter(
                    Q(user_receiving=account_id, user_sending=self.request.user)|
                    Q(user_receiving=self.request.user, user_sending=account_id)
                ).first() #only 1 relation is filtered here

                relation_to_change.relation_type=new_relation_type
                relation_to_change.save()

        return redirect('accounts:account_view', pk=account_id)


# class NotificationsView(LoginRequiredMixin, ListView):
#     model = Notification
#     template_name = 'accounts/notifications.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['seen_notifications'] = Notification.objects.filter(user=self.request.user, is_read=True)
#         context['unseen_notifications'] = Notification.objects.filter(user=self.request.user, is_read=False)
#         return context

#     def post(self, request, *args, **kwargs):
#         if "album_access_seen" in request.POST:
#             notif_to_update_id = request.POST['album_access_seen']
#             Notification.objects.filter(id=notif_to_update_id).update(is_read=True)
#             messages.success(self.request, f'Notification marked as seen')

#         if "relation_request_seen" in request.POST:
#             notif_to_update_id = request.POST['relation_request_seen']
#             Notification.objects.filter(id=notif_to_update_id).update(is_read=True)
#             messages.success(self.request, f'Notification marked as seen')

#         if "delete_notif" in request.POST:
#             notif_to_delete_id = request.POST['delete_notif']
#             notif_to_delete = Notification.objects.get(id=notif_to_delete_id)
#             if notif_to_delete:
#                 messages.success(self.request, f"Notification deleted successfully")
#                 notif_to_delete.delete()

#         return redirect('accounts:notifications_view')
