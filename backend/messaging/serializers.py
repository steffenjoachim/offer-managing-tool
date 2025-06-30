from rest_framework import serializers
from .models import Conversation, Message
from ads.models import Listing
from django.contrib.auth import get_user_model
from ads.serializers import ListingSerializer

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
        fields = ['id', 'sender', 'recipient', 'content', 'created_at', 'is_read', 'listing', 'file']
        read_only_fields = ['sender', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    listing = ListingSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()
    unreadCount = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'listing', 'created_at', 'updated_at', 'last_message', 'messages', 'unreadCount']

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-created_at').first()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None

    def get_messages(self, obj):
        # Alle Nachrichten der Konversation, sortiert nach created_at (aufsteigend)
        msgs = obj.messages.order_by('created_at')
        return MessageSerializer(msgs, many=True).data

    def get_unreadCount(self, obj):
        user = self.context['request'].user
        return obj.messages.filter(is_read=False, recipient=user).count()

class MessageCreateSerializer(serializers.ModelSerializer):
    # Serializer zum Erstellen von Nachrichten
    class Meta:
        model = Message
        fields = [
            'content',
            'file'
        ]
        extra_kwargs = {
            'content': {'required': False, 'allow_blank': True},
            'file': {'required': False, 'allow_null': True},
        }
        read_only_fields = ['empfaenger', 'anzeige'] # Empfänger und Anzeige werden vom Viewset gesetzt
        # Sender und timestamp werden im View automatisch gesetzt 