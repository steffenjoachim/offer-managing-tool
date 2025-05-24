from django.db import models
from django.conf import settings

class Anzeige(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='anzeigen')
    titel = models.CharField(max_length=200)
    beschreibung = models.TextField()
    preis = models.DecimalField(max_digits=10, decimal_places=2)
    erstellungsdatum = models.DateTimeField(auto_now_add=True)
    kategorie = models.CharField(max_length=100)
    STATUS_CHOICES = [
        ('aktiv', 'Aktiv'),
        ('verkauft', 'Verkauft'),
        ('deaktiviert', 'Deaktiviert'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aktiv')

    class Meta:
        verbose_name = 'Anzeige'
        verbose_name_plural = 'Anzeigen'

    def __str__(self):
        return self.titel

class AnzeigeBild(models.Model):
    anzeige = models.ForeignKey(Anzeige, related_name='bilder', on_delete=models.CASCADE)
    bild = models.ImageField(upload_to='anzeigen_bilder/')

    def __str__(self):
        return f"Bild für {self.anzeige.titel}"
