import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import LSA_Profile
from .serializers import BookingRequestSerializer
from .services import verify_booking_with_external_service

logger = logging.getLogger(__name__)

class BookingCreateAPIView(APIView):
    def post(self, request):
        serializer = BookingRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking = serializer.save()
        verification = verify_booking_with_external_service(booking)

        logger.info("Booking %s created successfully", booking.id)
        return Response(
            {
                "success": True,
                "message": "Booking request created successfully.",
                "booking": BookingRequestSerializer(booking).data,
                "verification": verification,
            },
            status=status.HTTP_201_CREATED,
        )

class LSASearchAPIView(APIView):
    def get(self, request):
        skill = request.query_params.get("skill")

        queryset = LSA_Profile.objects.filter(is_available=True)
        if skill:
            queryset = queryset.filter(skills__icontains=skill)

        queryset = queryset.only(
            "id", "name", "email", "phone", "skills", "is_available"
        )

        data = [
            {
                "id": lsa.id,
                "name": lsa.name,
                "email": lsa.email,
                "phone": lsa.phone,
                "skills": lsa.skills,
                "is_available": lsa.is_available,
            }
            for lsa in queryset
        ]

        return Response({
            "success": True,
            "count": len(data),
            "results": data,
        })
