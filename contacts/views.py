from django.shortcuts import render

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from .models import Contact
from .serializers import ContactSerializer


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    # Part 4: Support filtering by ?is_favorite=True/False (Django maps this easily)
    filterset_fields = ['is_favorite']
    # Part 4: Support ?search=john
    search_fields = ['first_name', 'last_name', 'email', 'personal_note']

    def get_queryset(self):
        # Ensure authenticated user only sees their own contacts
        return Contact.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Part 3: List favorite contacts GET /api/contacts/favorites
    @action(detail=False, methods=['get'])
    def favorites(self, request):
        queryset = self.filter_queryset(self.get_queryset().filter(is_favorite=True))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Part 3: Toggle favorite POST/DELETE /api/contacts/{id}/favorite
    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        contact = self.get_object()
        if request.method == 'POST':
            contact.is_favorite = True
        elif request.method == 'DELETE':
            contact.is_favorite = False

        contact.save()
        return Response(self.get_serializer(contact).data, status=status.HTTP_200_OK)

    # Part 3: Update note PUT/PATCH /api/contacts/{id}/note
    @action(detail=True, methods=['put', 'patch'])
    def note(self, request, pk=None):
        contact = self.get_object()
        note = request.data.get('personal_note')

        if note is not None:
            contact.personal_note = note
            contact.save()
            return Response(self.get_serializer(contact).data, status=status.HTTP_200_OK)
        return Response({"error": "personal_note field is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Part 5: Statistics API GET /api/contacts/stats
    @action(detail=False, methods=['get'])
    def stats(self, request):
        # Efficient DB query as requested, avoiding loading into memory
        stats = self.get_queryset().aggregate(
            total_contacts=Count('id'),
            favorite_contacts=Count('id', filter=Q(is_favorite=True)),
            contacts_with_notes=Count('id', filter=Q(personal_note__isnull=False) & ~Q(personal_note=''))
        )
        return Response(stats, status=status.HTTP_200_OK)