from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from contacts.models import Contact
from faker import Faker
import random


class Command(BaseCommand):
    help = 'Seeds the database with default test data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create a test user if it doesn't exist
        user, created = User.objects.get_or_create(username='testuser', email='test@envobyte.com')
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created testuser with password "password123"'))

        self.stdout.write('Seeding contacts...')

        contacts_to_create = []
        for _ in range(50):  # Generate 50 fake contacts
            contact = Contact(
                user=user,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                is_favorite=random.choice([True, False, False]),  # 33% chance of being favorite
                personal_note=fake.sentence() if random.choice([True, False]) else None
            )
            contacts_to_create.append(contact)

        Contact.objects.bulk_create(contacts_to_create)
        self.stdout.write(self.style.SUCCESS('Successfully seeded 50 contacts!'))