from rest_framework import serializers
from .models import Anzeige, AnzeigeBild
from django.contrib.auth import get_user_model

User = get_user_model()

class AnzeigeBildSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnzeigeBild
        fields = ['bild']

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'date_joined']

class AnzeigeSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    bilder = AnzeigeBildSerializer(many=True, read_only=True)

    class Meta:
        model = Anzeige
        fields = ['id', 'titel', 'beschreibung', 'preis', 'kategorie', 'bilder', 'user', 'erstellungsdatum']
        read_only_fields = ['erstellungsdatum'] 