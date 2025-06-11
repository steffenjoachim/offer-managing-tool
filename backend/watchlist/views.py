from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ads.models import Anzeige
from .models import WatchlistItem
from .serializers import WatchlistItemSerializer

class WatchlistListCreateView(generics.ListCreateAPIView):
    serializer_class = WatchlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WatchlistItem.objects.filter(user=self.request.user).order_by('-added_at')

    def perform_create(self, serializer):
        listing_id = self.request.data.get('listing_id')
        if not listing_id:
            raise serializers.ValidationError({'listing_id': 'This field is required.'})

        listing = get_object_or_404(Anzeige, id=listing_id)

        # Check if item already exists in watchlist
        if WatchlistItem.objects.filter(user=self.request.user, listing=listing).exists():
            return Response({'detail': 'Listing already in watchlist.'}, status=status.HTTP_409_CONFLICT)

        serializer.save(user=self.request.user, listing=listing)

class WatchlistDestroyView(generics.DestroyAPIView):
    serializer_class = WatchlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WatchlistItem.objects.filter(user=self.request.user)

    def get_object(self):
        listing_id = self.kwargs.get('listing_id')
        if not listing_id:
            raise serializers.ValidationError({'listing_id': 'Listing ID is required for deletion.'})
        
        obj = get_object_or_404(self.get_queryset(), listing__id=listing_id)
        return obj 