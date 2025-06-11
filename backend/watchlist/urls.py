from django.urls import path
from .views import WatchlistListCreateView, WatchlistDestroyView

urlpatterns = [
    path('items/', WatchlistListCreateView.as_view(), name='watchlist-list-create'),
    path('items/<int:listing_id>/remove/', WatchlistDestroyView.as_view(), name='watchlist-destroy'),
] 