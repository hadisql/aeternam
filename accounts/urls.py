from django.urls import path

from .views import UserUpdateView, UserView, RegisterPage, loginpage, NotificationsView
from django.contrib.auth.views import LogoutView

app_name =  "accounts"

urlpatterns = [
    path('register/', RegisterPage.as_view(), name='register'),
    path('login/', loginpage, name='login' ),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('edit/<int:pk>', UserUpdateView.as_view(), name='edit_account'),
    path('<int:pk>', UserView.as_view(), name='account_view' ),
    path('notifications/', NotificationsView.as_view(), name='notifications_view' ),
]
