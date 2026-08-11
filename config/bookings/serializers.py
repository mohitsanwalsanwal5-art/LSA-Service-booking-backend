from rest_framework import serializers
from .models import Booking_Request

class BookingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking_Request
        fields = [
            "id", "parent", "lsa", "service_date", "service_time",
            "status", "notes", "created_at"
        ]
        read_only_fields = ["id", "status", "created_at"]

    def validate(self, data):
        if not data["lsa"].is_available:
            raise serializers.ValidationError(
                {"lsa": "Selected LSA is currently unavailable."}
            )
        return data
