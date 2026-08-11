from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Parent, LSA_Profile, Booking_Request

class BookingAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.parent = Parent.objects.create(
            name="Rahul Parent",
            email="parent@example.com",
            phone="9876543210",
        )
        self.lsa = LSA_Profile.objects.create(
            name="Anita Sharma",
            email="lsa@example.com",
            phone="9876500000",
            skills=["Autism", "Speech Therapy"],
            is_available=True,
        )
        self.unavailable_lsa = LSA_Profile.objects.create(
            name="Unavailable LSA",
            email="unavailable@example.com",
            phone="9999999999",
            skills=["Autism"],
            is_available=False,
        )

    @patch("bookings.views.verify_booking_with_external_service")
    def test_create_booking_success(self, mock_service):
        mock_service.return_value = {"success": True}
        response = self.client.post(
            "/api/v1/bookings/",
            {
                "parent": self.parent.id,
                "lsa": self.lsa.id,
                "service_date": "2026-08-15",
                "service_time": "10:30:00",
                "notes": "Test booking",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking_Request.objects.count(), 1)

    def test_create_booking_missing_parent(self):
        response = self.client.post(
            "/api/v1/bookings/",
            {
                "lsa": self.lsa.id,
                "service_date": "2026-08-15",
                "service_time": "10:30:00",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_create_booking_unavailable_lsa(self):
        response = self.client.post(
            "/api/v1/bookings/",
            {
                "parent": self.parent.id,
                "lsa": self.unavailable_lsa.id,
                "service_date": "2026-08-15",
                "service_time": "10:30:00",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_lsa_search_by_skill(self):
        response = self.client.get("/api/v1/lsas/search/?skill=Autism")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_lsa_search_only_available(self):
        response = self.client.get("/api/v1/lsas/search/?skill=Autism")
        for lsa in response.data["results"]:
            self.assertTrue(lsa["is_available"])

    def test_lsa_search_without_skill(self):
        response = self.client.get("/api/v1/lsas/search/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
