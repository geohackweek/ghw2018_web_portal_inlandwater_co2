from apps.home.views import index

from django.urls import path

urlpatterns = [
    path('', index, name='home_page')
]