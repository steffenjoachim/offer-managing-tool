from rest_framework import serializers
from .models import WatchlistItem
from ads.serializers import AnzeigeSerializer

class WatchlistItemSerializer(serializers.ModelSerializer):
    listing = AnzeigeSerializer(read_only=True) # AnzeigeSerializer einbetten

    class Meta:
        model = WatchlistItem
        fields = ['id', 'user', 'listing', 'added_at']
        read_only_fields = ['user', 'added_at'] 