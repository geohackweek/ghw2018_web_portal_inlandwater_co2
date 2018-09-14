from apps.co2data.views import data

from django.urls import path

urlpatterns = [
    path('', data, name='data_page')
]
