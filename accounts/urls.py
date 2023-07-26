from django.urls import path

from .views import UserUpdateView, UserView

app_name =  "accounts"

urlpatterns = [
    path('edit/<int:pk>', UserUpdateView.as_view(), name='edit_account'),
    path('<int:pk>', UserView.as_view(), name='account_view' )
]
