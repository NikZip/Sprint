from django.urls import path
from .views import *

urlpatterns = [
    path('perivals', ArtsApiView.as_view(), name='passes'),
]