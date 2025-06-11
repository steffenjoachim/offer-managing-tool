from django.shortcuts import render
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Message, Conversation
from ads.models import Anzeige # Importiere das Anzeigen-Modell
from .serializers import MessageSerializer, MessageCreateSerializer, ConversationSerializer
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser

User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.conversations.all()

    def perform_create(self, serializer):
        print(f"Debug: Erstelle neue Konversation mit Daten: {serializer.validated_data}")
        conversation = serializer.save()
        
        # Füge den aktuellen Benutzer als Teilnehmer hinzu
        conversation.participants.add(self.request.user)
        print(f"Debug: Aktueller Benutzer {self.request.user.username} als Teilnehmer hinzugefügt")
        
        # Wenn die Konversation mit einer Anzeige verknüpft ist, füge den Anzeigen-Ersteller als Teilnehmer hinzu
        if conversation.listing:
            if self.request.user == conversation.listing.user:
                # Verhindere, dass der Benutzer eine Konversation mit sich selbst für die eigene Anzeige erstellt
                conversation.delete() # Die soeben erstellte Konversation löschen
                raise serializers.ValidationError("Sie können keine Konversation für Ihre eigene Anzeige erstellen, es sei denn, ein anderer Benutzer initiiert sie.")

            print(f"Debug: Konversation ist mit Anzeige {conversation.listing.id} verknüpft")
            print(f"Debug: Anzeigen-Ersteller ist {conversation.listing.user.username}")
            conversation.participants.add(conversation.listing.user)
            print(f"Debug: Anzeigen-Ersteller als Teilnehmer hinzugefügt")
        
        # Debug-Ausgabe der Teilnehmer
        print(f"Debug: Aktuelle Teilnehmer der Konversation: {[p.username for p in conversation.participants.all()]}")

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
    # serializer_class wird dynamisch in get_serializer_class bestimmt
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        return Message.objects.filter(conversation_id=conversation_id)

    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer

    def create(self, request, *args, **kwargs):
        print(f"Debug: MessageViewSet.create - Raw request.data: {request.data}")
        for key, value in request.data.items():
            print(f"Debug: MessageViewSet.create - Key: {key}, Value: {value}, Type: {type(value)}")

        # Manually construct data that the serializer should process
        data_for_serializer = {}
        if 'text' in request.data:
            data_for_serializer['text'] = request.data['text']
        if 'file' in request.data:
            data_for_serializer['file'] = request.data['file']
        
        print(f"Debug: MessageViewSet.create - Data passed to serializer: {data_for_serializer}")
        
        # Übergebe die modifizierten Daten an den Serializer
        serializer = self.get_serializer(data=data_for_serializer)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, id=conversation_id)
        
        print(f"Debug: perform_create - Starte für Konversation {conversation_id}")
        print(f"Debug: perform_create - Aktuelle Teilnehmer: {[p.username for p in conversation.participants.all()]}")
        print(f"Debug: perform_create - Request user: {self.request.user.username}, ID: {self.request.user.id}")

        # Bestimme den Empfänger der Nachricht
        empfaenger = conversation.participants.exclude(id=self.request.user.id).first()
        
        # Für Nachrichten, die an eine bestehende Konversation gesendet werden,
        # sollte das `anzeige`-Feld aus dem Listing der Konversation stammen.
        anzeige = conversation.listing if conversation.listing else None

        print(f"Debug: perform_create - Gefundener Empfänger: {empfaenger.username if empfaenger else 'Kein Empfänger gefunden (None)'}")
        print(f"Debug: perform_create - Verknüpfte Anzeige: {anzeige.titel if anzeige else 'Keine Anzeige verknüpft'}")

        if not empfaenger:
            print(f"Debug: perform_create - Fehler: Kein Empfänger gefunden, obwohl erwartet.")
            raise serializers.ValidationError({"empfaenger": ["Konversation hat keinen gültigen Empfänger (nur einen Teilnehmer)."]})

        # Add debug for validated_data
        print(f"Debug: perform_create - Validated Data before save: {serializer.validated_data}")

        # Save the message with determined sender, conversation, and recipient
        serializer.save(sender=self.request.user, conversation=conversation, empfaenger=empfaenger, anzeige=anzeige)
        print(f"Debug: perform_create - Nachricht erfolgreich in DB gespeichert.")

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
        Erwartet: listingId, content (text) oder file.
        """
        listing_id = request.data.get('listingId')
        content = request.data.get('content')
        file = request.data.get('file')

        if not listing_id:
            return Response({'detail': 'listingId ist erforderlich.'}, status=status.HTTP_400_BAD_REQUEST)

        if not content and not file:
            return Response({'detail': 'Nachrichtentext oder Datei ist erforderlich.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            anzeige = Anzeige.objects.get(id=listing_id)
            sender = request.user

            # Die beiden Kernparteien sind der Sender und der Ersteller der Anzeige.
            user1 = sender
            user2 = anzeige.user

            # Bestimme den Empfänger basierend auf den Teilnehmern der Konversation.
            if sender == anzeige.user:
                other_participants = Conversation.objects.filter(
                    listing=anzeige,
                    participants=sender
                ).exclude(participants=sender).first()

                if other_participants:
                    conversation = other_participants
                    empfaenger = conversation.participants.exclude(id=sender.id).first()
                else:
                    print(f"Versuch, Nachricht als Anzeigen-Ersteller {sender.username} zu senden, aber kein anderer Teilnehmer in Konversation für Anzeige {anzeige.id} gefunden.")
                    return Response({'detail': 'Sie können keine Nachricht an sich selbst senden, solange kein anderer Benutzer eine Konversation initiiert hat.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                empfaenger = anzeige.user
                conversation, created = Conversation.objects.get_or_create(listing=anzeige)
                conversation.participants.add(user1, user2)

            # Erstelle die neue Nachricht
            message = Message.objects.create(
                conversation=conversation,
                sender=sender,
                empfaenger=empfaenger,
                text=content,
                file=file,
            )

            # Serialisiere die erstellte Nachricht und gib sie zurück
            serializer = MessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Anzeige.DoesNotExist:
            return Response({'detail': 'Anzeige nicht gefunden.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Fehler beim Senden der Nachricht: {e}")
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
