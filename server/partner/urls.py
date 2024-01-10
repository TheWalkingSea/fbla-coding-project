from django.urls import path
from .views import (
    PartnerListCreateView, PartnerRetrieveUpdateDestroyView,
    PartnerTagListCreateView, PartnerTagRetrieveUpdateDestroyView
)

urlpatterns = [
    path('', PartnerListCreateView.as_view(), name='partner-list-create'),
    path('<int:pk>/', PartnerRetrieveUpdateDestroyView.as_view(), name='partner-retrieve-update-destroy'),
    
    path('tags/', PartnerTagListCreateView.as_view(), name='partnertag-list-create'),
    path('tags/<int:pk>/', PartnerTagRetrieveUpdateDestroyView.as_view(), name='partnertag-retrieve-update-destroy'),
]