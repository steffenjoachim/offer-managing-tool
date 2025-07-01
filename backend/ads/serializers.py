from rest_framework import serializers
from .models import Listing, ListingImage
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']

class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['id', 'image', 'created_at']

class ListingSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)
    user = SimpleUserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_expired = serializers.SerializerMethodField()
    valid_until = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'user', 'title', 'description', 'price', 'category',
            'images', 'created_at', 'updated_at', 'is_expired',
            'valid_until',
        ]
        read_only_fields = ['user', 'created_at', 'updated_at', 'valid_until']

    def get_is_expired(self, obj):
        if not obj.created_at:
            return False
        expiration_date = obj.created_at + timezone.timedelta(days=30)
        return timezone.now() > expiration_date

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return value

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long")
        if len(value) > 200:
            raise serializers.ValidationError("Title cannot exceed 200 characters")
        return value

    def validate_description(self, value):
        return value

    def create(self, validated_data):
        try:
            images_data = self.context.get('request').FILES.getlist('images')
            listing = Listing.objects.create(**validated_data)
            
            for image_data in images_data:
                ListingImage.objects.create(listing=listing, image=image_data)
            
            return listing
        except Exception as e:
            raise serializers.ValidationError(f"Error creating listing: {str(e)}")

    def update(self, instance, validated_data):
        try:
            images_data = self.context.get('request').FILES.getlist('images')

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            request = self.context.get('request')
            if (images_data and len(images_data) > 0):
                instance.images.all().delete()
                for image_data in images_data:
                    ListingImage.objects.create(listing=instance, image=image_data)
            elif request and request.data.get('images') == '[]':
                instance.images.all().delete()

            return instance
        except Exception as e:
            raise serializers.ValidationError(f"Error updating listing: {str(e)}") 