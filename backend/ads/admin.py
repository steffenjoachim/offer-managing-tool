from django.contrib import admin
from .models import Anzeige, AnzeigeBild

class AnzeigeBildInline(admin.TabularInline):
    model = AnzeigeBild
    extra = 1

@admin.register(Anzeige)
class AnzeigeAdmin(admin.ModelAdmin):
    list_display = ('titel', 'user', 'preis', 'erstellungsdatum', 'status')
    list_filter = ('status', 'kategorie')
    search_fields = ('titel', 'beschreibung', 'user__username')
    date_hierarchy = 'erstellungsdatum'
    inlines = [AnzeigeBildInline]
