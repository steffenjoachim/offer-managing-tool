from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from ads.models import Anzeige

User = get_user_model()

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    empfaenger = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages',
        verbose_name='Empfänger'
    )
    anzeige = models.ForeignKey(
        Anzeige,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Anzeige',
        null=True,
        blank=True
    )
    text = models.TextField(verbose_name='Nachrichtentext')
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False, verbose_name='Gelesen')

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Nachricht'
        verbose_name_plural = 'Nachrichten'

    def __str__(self):
        return f"Nachricht von {self.sender.username} an {self.empfaenger.username} ({self.timestamp})"
