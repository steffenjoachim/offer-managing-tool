from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone

User = get_user_model()

class Listing(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('home', 'Home & Garden'),
        ('sports', 'Sports & Leisure'),
        ('toys', 'Toys & Games'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    favorites_count = models.PositiveIntegerField(default=0)
    # Ablaufdatum der Anzeige, kann für Verlängerungen genutzt werden
    valid_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['category']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.title} - {self.price}"

    def save(self, *args, **kwargs):
        # Setze valid_until beim ersten Speichern auf jetzt + 3 Tage, falls nicht gesetzt
        if not self.valid_until:
            basis = self.created_at if self.created_at else timezone.now()
            self.valid_until = basis + timezone.timedelta(days=3)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        # Nutze valid_until für die Ablaufprüfung
        if not self.valid_until:
            return False
        return timezone.now() > self.valid_until

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def increment_favorites(self):
        self.favorites_count += 1
        self.save(update_fields=['favorites_count'])

    def decrement_favorites(self):
        if self.favorites_count > 0:
            self.favorites_count -= 1
            self.save(update_fields=['favorites_count'])

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Image for {self.listing.title}"
