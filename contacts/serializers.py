from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'email', 'is_favorite', 'personal_note', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']