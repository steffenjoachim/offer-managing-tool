from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Listing, ListingImage
from .serializers import ListingSerializer, ListingImageSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, BasePermission, SAFE_METHODS
from rest_framework.permissions import IsAuthenticated
import logging
from rest_framework.views import APIView
from django.utils import timezone

logger = logging.getLogger(__name__)

# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class IsOwnerOrReadOnly(BasePermission):
    """
    Erlaubt Bearbeiten/Löschen nur für den Besitzer, Lesen für alle.
    """
    def has_object_permission(self, request, view, obj):
        # Lesen ist für alle erlaubt
        if request.method in SAFE_METHODS:
            return True
        # Schreiben/Bearbeiten/Löschen nur für den Besitzer
        return obj.user == request.user

class ListingListCreateView(generics.ListCreateAPIView):
    queryset = Listing.objects.all().order_by('-created_at')
    serializer_class = ListingSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        try:
            queryset = super().get_queryset()
            # Zeige nur gültige Anzeigen (valid_until in der Zukunft)
            queryset = queryset.filter(valid_until__gt=timezone.now())
            if self.request.path.endswith('my/'):
                queryset = queryset.filter(user=self.request.user)
            return queryset
        except Exception as e:
            logger.error(f"Error in get_queryset: {str(e)}")
            raise

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error in list view: {str(e)}")
            return Response(
                {'detail': f'Error retrieving listings: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            self.perform_create(serializer)
            listing_instance = serializer.instance
            
            response_serializer = self.get_serializer(listing_instance)
            
            headers = self.get_success_headers(response_serializer.data)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.error(f"Error in create view: {str(e)}")
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class ListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsOwnerOrReadOnly | IsAuthenticatedOrReadOnly]

# Verlängerungs-API für Listings
class ExtendListingValidityView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            listing = Listing.objects.get(pk=pk)
            if listing.user != request.user:
                return Response({'detail': 'Nicht berechtigt.'}, status=status.HTTP_403_FORBIDDEN)
            # Setze valid_until auf jetzt + 3 Tage (egal wie weit in der Zukunft)
            listing.valid_until = timezone.now() + timezone.timedelta(days=3)
            listing.save()
            return Response({'valid_until': listing.valid_until}, status=status.HTTP_200_OK)
        except Listing.DoesNotExist:
            return Response({'detail': 'Anzeige nicht gefunden.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Fehler bei Verlängerung: {str(e)}")
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
