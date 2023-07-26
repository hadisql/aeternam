from django.urls import path

import core.views

app_name = "core"

urlpatterns = [
    path('', core.views.index, name='index')
]
