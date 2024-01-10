from django.urls import path
from .views import (
    OrganizationListCreateView, OrganizationRetrieveUpdateDestroyView,
    OrganizationTagListCreateView, OrganizationTagRetrieveUpdateDestroyView
)

urlpatterns = [
    path('', OrganizationListCreateView.as_view(), name='organization-list-create'),
    path('<int:pk>/', OrganizationRetrieveUpdateDestroyView.as_view(), name='organization-retrieve-update-destroy'),
    
    path('tags/', OrganizationTagListCreateView.as_view(), name='organizationtag-list-create'),
    path('tags/<int:pk>/', OrganizationTagRetrieveUpdateDestroyView.as_view(), name='organizationtag-retrieve-update-destroy'),
]