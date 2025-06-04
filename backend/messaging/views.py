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

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """
        Marks all unread messages in a conversation for the requesting user as read.
        """
        conversation = self.get_object()
        # Markieren Sie alle Nachrichten in dieser Konversation, die NICHT vom anfragenden Benutzer gesendet wurden
        # und noch nicht gelesen sind, als gelesen.
        messages_to_mark = conversation.messages.filter(
            is_read=False,
            empfaenger=request.user # Nur Nachrichten markieren, wo der aktuelle Benutzer der Empfänger ist
        )
        count_updated = messages_to_mark.update(is_read=True)
        
        return Response({'status': f'{count_updated} messages marked as read'})

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
    def mark_as_read(self, request, pk=None):
        """
        Marks all unread messages in a conversation for the requesting user as read.
        """
        conversation = self.get_object()
        # Markieren Sie alle Nachrichten in dieser Konversation, die NICHT vom anfragenden Benutzer gesendet wurden
        # und noch nicht gelesen sind, als gelesen.
        messages_to_mark = conversation.messages.filter(
            is_read=False,
            empfaenger=request.user # Nur Nachrichten markieren, wo der aktuelle Benutzer der Empfänger ist
        )
        count_updated = messages_to_mark.update(is_read=True)

        return Response({'status': f'{count_updated} messages marked as read'})

    @action(detail=False, methods=['post'])
    def send_message(self, request):
        """
        Sendet eine neue Nachricht im Kontext einer Anzeige.
        Erwartet: listingId, content.
        """
        listing_id = request.data.get('listingId')
        content = request.data.get('content')

        if not listing_id or not content:
            return Response({'detail': 'listingId und content sind erforderlich.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            anzeige = Anzeige.objects.get(id=listing_id)
            sender = request.user

            # Die beiden Kernparteien sind der Sender und der Ersteller der Anzeige.
            user1 = sender
            user2 = anzeige.user

            # 1. Finde oder erstelle Konversation, die mit dieser Anzeige verknüpft ist.
            conversation, created = Conversation.objects.get_or_create(listing=anzeige)

            # 2. Füge beide Kernparteien als Teilnehmer hinzu (add ist idempotent).
            conversation.participants.add(user1, user2)

            # 3. Bestimme den Empfänger basierend auf den Teilnehmern der Konversation.
            # Wenn der Sender der Ersteller der Anzeige ist:
            if sender == anzeige.user:
                # Finde den anderen Teilnehmer in der Konversation.
                other_participants = conversation.participants.exclude(id=sender.id)
                if other_participants.exists():
                    empfaenger = other_participants.first()
                else:
                    # Dieser Fall tritt auf, wenn der Sender der Ersteller der Anzeige ist
                    # und noch kein anderer Teilnehmer der Konversation hinzugefügt wurde.
                    # Dies sollte verhindert werden, da der Ersteller keine Nachricht an sich selbst senden kann.
                    print(f"Versuch, Nachricht als Anzeigen-Ersteller {sender.username} zu senden, aber kein anderer Teilnehmer in Konversation {conversation.id} gefunden.")
                    return Response({'detail': 'Sie können keine Nachricht an sich selbst senden, solange kein anderer Benutzer eine Konversation initiiert hat.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Der Sender ist NICHT der Ersteller der Anzeige. Der Empfänger ist der Ersteller der Anzeige.
                empfaenger = anzeige.user

            # Erstelle die neue Nachricht
            message = Message.objects.create(
                conversation=conversation,
                sender=sender,
                empfaenger=empfaenger, # Der korrekt bestimmte Empfänger
                text=content,
                # timestamp wird automatisch gesetzt
            )

            # Serialisiere die erstellte Nachricht und gib sie zurück
            serializer = MessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Anzeige.DoesNotExist:
            return Response({'detail': 'Anzeige nicht gefunden.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Loggen Sie den Fehler für Debugging
            print(f"Fehler beim Senden der Nachricht: {e}")
            # Hier wird ein allgemeiner 500-Fehler zurückgegeben, der die genaue Ursache verschleiert.
            # Wir sollten sicherstellen, dass spezifischere Fehler vorher abgefangen werden.
            return Response({'detail': 'Ein interner Serverfehler ist beim Senden der Nachricht aufgetreten.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def by_anzeige(self, request):
        # Gibt Nachrichten zurück, die sich auf eine bestimmte Anzeige beziehen
        anzeige_id = request.query_params.get('anzeige_id', None)
        if not anzeige_id:
            return Response({'detail': 'Bitte geben Sie eine anzeige_id an.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            anzeige = Anzeige.objects.get(id=anzeige_id)
            # Stelle sicher, dass der Benutzer berechtigt ist
            if anzeige.user == request.user or Conversation.objects.filter(listing=anzeige, participants=request.user).exists():
                # Finde die Konversation für diese Anzeige und den aktuellen Benutzer
                conversation = Conversation.objects.filter(listing=anzeige, participants=request.user).first()
                if conversation:
                     messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
                     serializer = self.get_serializer(messages, many=True)
                     return Response(serializer.data)
                else:
                     return Response({'detail': 'Keine Konversation für diese Anzeige gefunden.'}, status=status.HTTP_404_NOT_FOUND)

            else:
                 return Response({'detail': 'Sie sind nicht berechtigt, Nachrichten für diese Anzeige anzuzeigen.'}, status=status.HTTP_403_FORBIDDEN)

        except Anzeige.DoesNotExist:
            return Response({'detail': 'Anzeige nicht gefunden.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        conversation = get_object_or_404(Conversation, pk=pk)
        # Stelle sicher, dass der Benutzer Teilnehmer der Konversation ist
        if request.user in conversation.participants.all():
            messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
            serializer = self.get_serializer(messages, many=True)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Sie sind kein Teilnehmer dieser Konversation.'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['delete'])
    def delete(self, request, pk=None):
         conversation = get_object_or_404(Conversation, pk=pk)
         # Nur Teilnehmer der Konversation dürfen sie löschen
         if request.user in conversation.participants.all():
             conversation.delete()
             return Response(status=status.HTTP_204_NO_CONTENT)
         else:
             return Response({'detail': 'Sie sind nicht berechtigt, diese Konversation zu löschen.'}, status=status.HTTP_403_FORBIDDEN)
