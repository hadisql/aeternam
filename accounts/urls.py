from django.urls import path

from .views import UserUpdateView, UserView, RegisterPage, loginpage, activate_account
from django.contrib.auth.views import LogoutView

app_name =  "accounts"

urlpatterns = [
    path('register/', RegisterPage.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),
    path('login/', loginpage, name='login' ),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('edit/<int:pk>', UserUpdateView.as_view(), name='edit_account'),
    path('<int:pk>', UserView.as_view(), name='account_view' ),
]
