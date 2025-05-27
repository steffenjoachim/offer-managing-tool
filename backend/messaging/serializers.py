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

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'updated_at', 'last_message']

    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return MessageSerializer(last_message).data
        return None

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