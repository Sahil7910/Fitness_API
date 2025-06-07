from django.test import TestCase
from django.utils import timezone
from .models import FitnessClass, Booking
from rest_framework.test import APIClient
from rest_framework import status
from datetime import timedelta

class BookingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.fitness_class = FitnessClass.objects.create(
            name='Zumba',
            datetime=timezone.now() + timedelta(days=1),
            instructor='Instructor X',
            available_slots=5
        )

    def test_list_classes(self):
        response = self.client.get('/classes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_successful_booking(self):
        data = {
            "class_id": self.fitness_class.id,
            "client_name": "Test User",
            "client_email": "test@example.com"
        }
        response = self.client.post('/book/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

    def test_booking_when_full(self):
        self.fitness_class.available_slots = 0
        self.fitness_class.save()
        data = {
            "class_id": self.fitness_class.id,
            "client_name": "User",
            "client_email": "full@example.com"
        }
        response = self.client.post('/book/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No available slots.", str(response.content))

    def test_get_bookings_by_email(self):
        Booking.objects.create(
            fitness_class=self.fitness_class,
            client_name="User A",
            client_email="usera@example.com"
        )
        response = self.client.get('/bookings/?email=usera@example.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
