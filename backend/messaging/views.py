from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Message, Conversation
from ads.models import Anzeige # Importiere das Anzeigen-Modell
from .serializers import MessageSerializer, MessageCreateSerializer, ConversationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.conversations.all()

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, id=user_id)
        conversation.participants.add(user)
        return Response(self.get_serializer(conversation).data)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        return Message.objects.filter(conversation_id=conversation_id)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, id=conversation_id)
        serializer.save(sender=self.request.user, conversation=conversation)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None, conversation_pk=None):
        message = self.get_object()
        message.is_read = True
        message.save()
        return Response(self.get_serializer(message).data)

    # Optional: Aktion zum Abrufen von Nachrichten für eine bestimmte Anzeige
    @action(detail=False, methods=['get'])
    def by_anzeige(self, request):
        # Gibt Nachrichten zurück, die sich auf eine bestimmte Anzeige beziehen
        anzeige_id = request.query_params.get('anzeige_id', None)
        if not anzeige_id:
            return Response({'detail': 'Bitte geben Sie eine anzeige_id an.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Stelle sicher, dass der Benutzer berechtigt ist, die Nachrichten dieser Anzeige zu sehen
        # (entweder Ersteller der Anzeige oder Absender/Empfänger einer Nachricht bzgl. dieser Anzeige)
        try:
            anzeige = Anzeige.objects.get(id=anzeige_id)
            # Benutzer ist Ersteller der Anzeige ODER
            # Benutzer hat Nachrichten bzgl. dieser Anzeige
            if anzeige.user == request.user or Message.objects.filter(anzeige=anzeige, sender=request.user).exists() or Message.objects.filter(anzeige=anzeige, empfaenger=request.user).exists():
                messages = self.get_queryset().filter(anzeige=anzeige).order_by('timestamp')
                serializer = self.get_serializer(messages, many=True)
                return Response(serializer.data)
            else:
                 return Response({'detail': 'Sie sind nicht berechtigt, Nachrichten für diese Anzeige anzuzeigen.'}, status=status.HTTP_403_FORBIDDEN)

        except Anzeige.DoesNotExist:
            return Response({'detail': 'Anzeige nicht gefunden.'}, status=status.HTTP_404_NOT_FOUND)
