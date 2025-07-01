from django.urls import path
from .views import ListingListCreateView, ListingDetailView, ExtendListingValidityView

urlpatterns = [
    path('', ListingListCreateView.as_view(), name='listing-list-create'),
    path('my/', ListingListCreateView.as_view(), name='my-listings'),
    path('<int:pk>/', ListingDetailView.as_view(), name='listing-detail'),
    path('<int:pk>/extend/', ExtendListingValidityView.as_view(), name='listing-extend'),
] 