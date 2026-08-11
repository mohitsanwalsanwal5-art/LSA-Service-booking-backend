from django.urls import path
from .views import BookingCreateAPIView, LSASearchAPIView

urlpatterns = [
    path("api/v1/bookings/", BookingCreateAPIView.as_view(), name="booking-create"),
    path("api/v1/lsas/search/", LSASearchAPIView.as_view(), name="lsa-search"),
]
