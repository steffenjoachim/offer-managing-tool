from rest_framework import serializers
from .models import Conversation, Message
from ads.models import Listing
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'created_at', 'is_read', 'listing']
        read_only_fields = ['sender', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    listing = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'listing', 'created_at', 'updated_at']

class MessageCreateSerializer(serializers.ModelSerializer):
    # Serializer zum Erstellen von Nachrichten
    class Meta:
        model = Message
        fields = [
            'text',
            'file'
        ]
        extra_kwargs = {
            'text': {'required': False, 'allow_blank': True},
            'file': {'required': False, 'allow_null': True},
        }
        read_only_fields = ['empfaenger', 'anzeige'] # Empfänger und Anzeige werden vom Viewset gesetzt
        # Sender und timestamp werden im View automatisch gesetzt 