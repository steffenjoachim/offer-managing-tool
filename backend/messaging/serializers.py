from rest_framework import serializers
from .models import Conversation, Message
from ads.models import Anzeige
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    empfaenger = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'empfaenger', 'text', 'timestamp', 'is_read', 'anzeige', 'file']
        read_only_fields = ['sender', 'timestamp']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unreadCount = serializers.SerializerMethodField()
    listing = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'updated_at', 'last_message', 'unreadCount', 'listing', 'messages']

    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-timestamp').first()
        if last_message:
            return MessageSerializer(last_message).data
        return None

    def get_unreadCount(self, obj):
        user = self.context['request'].user
        unread_messages = obj.messages.filter(is_read=False, empfaenger=user)
        count = unread_messages.count()
        return count

    def get_listing(self, obj):
        if obj.listing:
            return {
                'id': obj.listing.id,
                'title': getattr(obj.listing, 'titel', getattr(obj.listing, 'title', ''))
            }
        return None

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