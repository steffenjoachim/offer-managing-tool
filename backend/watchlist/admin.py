from django.contrib import admin
from .models import WatchlistItem

@admin.register(WatchlistItem)
class WatchlistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'listing__titel') 