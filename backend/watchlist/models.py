from django.db import models
from django.conf import settings
from ads.models import Anzeige

class WatchlistItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watchlist_items')
    listing = models.ForeignKey(Anzeige, on_delete=models.CASCADE, related_name='in_watchlists')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')
        verbose_name = 'Merklisteneintrag'
        verbose_name_plural = 'Merklisteneinträge'

    def __str__(self):
        return f"{self.user.username} - {self.listing.titel}" 