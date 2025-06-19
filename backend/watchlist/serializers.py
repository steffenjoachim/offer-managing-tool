from rest_framework import serializers
from .models import WatchlistItem
from ads.serializers import ListingSerializer

class WatchlistItemSerializer(serializers.ModelSerializer):
    listing = ListingSerializer(read_only=True)

    class Meta:
        model = WatchlistItem
        fields = ['id', 'user', 'listing', 'added_at']
        read_only_fields = ['user', 'added_at'] 