from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Anzeige, AnzeigeBild
from .serializers import AnzeigeSerializer, AnzeigeBildSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.

class ListingListCreateView(generics.ListCreateAPIView):
    queryset = Anzeige.objects.all()
    serializer_class = AnzeigeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        anzeige_instance = serializer.instance
        
        bilder_data = request.FILES.getlist('bilder')
        if bilder_data:
            for bild_file in bilder_data:
                AnzeigeBild.objects.create(anzeige=anzeige_instance, bild=bild_file)

        response_serializer = self.get_serializer(anzeige_instance)
        
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Anzeige.objects.all()
    serializer_class = AnzeigeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
