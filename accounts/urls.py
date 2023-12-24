from django.urls import path, reverse_lazy

from .views import UserUpdateView, UserView, RegisterPage, loginpage, activate_account, ChangePasswordView
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from .forms import CustomPasswordResetForm, CustomSetPasswordForm

app_name =  "accounts"

urlpatterns = [
    path('register/', RegisterPage.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),
    path('login/', loginpage, name='login' ),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('edit/<int:pk>', UserUpdateView.as_view(), name='edit_account'),
    path('<int:pk>', UserView.as_view(), name='account_view' ),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('password-reset/', PasswordResetView.as_view(form_class=CustomPasswordResetForm, success_url=reverse_lazy('accounts:password_reset_done')), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(form_class=CustomSetPasswordForm, success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
