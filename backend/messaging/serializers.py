from rest_framework import serializers
from .models import Conversation, Message
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
        fields = ['id', 'sender', 'empfaenger', 'text', 'timestamp', 'is_read', 'anzeige']
        read_only_fields = ['sender', 'timestamp']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'updated_at', 'last_message', 'unread_count']

    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-timestamp').first()
        if last_message:
            return {
                'text': last_message.text,
                'timestamp': last_message.timestamp,
                'sender': UserSerializer(last_message.sender).data
            }
        return None

    def get_unread_count(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.messages.filter(empfaenger=user, is_read=False).count()
        return 0

class MessageCreateSerializer(serializers.ModelSerializer):
    # Serializer zum Erstellen von Nachrichten
    class Meta:
        model = Message
        fields = [
            'empfaenger',
            'anzeige',
            'text'
        ]
        # Sender und timestamp werden im View automatisch gesetzt 