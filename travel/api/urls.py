from django.urls import path
from .views import *

urlpatterns = [
    path('perivals', PassApiView.as_view(), name='passes'),
    path('perivals/<int:pk>', PassDetailApiView.as_view(), name='pass_detail'),
    path('perivals/search/', PassListQueryView.as_view(), name='pass_query'),
]