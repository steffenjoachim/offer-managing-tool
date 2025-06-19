from django.contrib import admin
from .models import Listing, ListingImage

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'created_at', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description', 'user__username')
    date_hierarchy = 'created_at'
    inlines = [ListingImageInline]

admin.site.register(Listing, ListingAdmin)
admin.site.register(ListingImage)
