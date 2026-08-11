 from django.db import models

class Parent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class LSA_Profile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    skills = models.JSONField(default=list)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Booking_Request(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    parent = models.ForeignKey(
        Parent, on_delete=models.CASCADE, related_name="booking_requests"
    )
    lsa = models.ForeignKey(
        LSA_Profile, on_delete=models.CASCADE, related_name="booking_requests"
    )
    service_date = models.DateField()
    service_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["lsa", "service_date", "service_time"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"Booking {self.id}"
