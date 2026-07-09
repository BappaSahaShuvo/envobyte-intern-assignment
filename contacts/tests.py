from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Contact


class ContactAPITests(APITestCase):
    def setUp(self):
        # Create user and authenticate
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)

        # Create base contact
        self.contact = Contact.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            personal_note="Initial note"
        )

    def test_mark_contact_as_favorite(self):
        """Test POST /api/contacts/{id}/favorite/"""
        url = f'/api/contacts/{self.contact.id}/favorite/'
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact.refresh_from_db()
        self.assertTrue(self.contact.is_favorite)

    def test_update_personal_note(self):
        """Test PATCH /api/contacts/{id}/note/"""
        url = f'/api/contacts/{self.contact.id}/note/'
        data = {'personal_note': 'Updated meeting notes.'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.personal_note, 'Updated meeting notes.')

    def test_filter_contacts_by_favorite(self):
        """Test GET /api/contacts/?is_favorite=True"""
        # Create an extra favorite contact
        Contact.objects.create(
            user=self.user,
            first_name="Jane",
            last_name="Smith",
            is_favorite=True
        )

        url = '/api/contacts/?is_favorite=True'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only return Jane (1 result) because John is not favorited by default
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['first_name'], 'Jane')
