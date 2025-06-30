from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Listing, ListingImage
from .serializers import ListingSerializer, ListingImageSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, BasePermission, SAFE_METHODS
import logging

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
