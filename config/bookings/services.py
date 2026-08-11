import logging
import requests

logger = logging.getLogger(__name__)

MOCK_SERVICE_URL = "https://example.com/api/verify"

def verify_booking_with_external_service(booking):
    payload = {
        "booking_id": booking.id,
        "parent_id": booking.parent_id,
        "lsa_id": booking.lsa_id,
        "service_date": str(booking.service_date),
        "service_time": str(booking.service_time),
    }

    try:
        response = requests.post(MOCK_SERVICE_URL, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()
        logger.info("External verification successful for booking %s", booking.id)
        return data
    except requests.exceptions.Timeout:
        logger.error("External service timeout for booking %s", booking.id)
        return {"success": False, "error": "External service timeout"}
    except requests.exceptions.RequestException as exc:
        logger.exception("External service failed for booking %s: %s", booking.id, exc)
        return {"success": False, "error": "External service unavailable"}
    except ValueError:
        logger.error("Invalid JSON response for booking %s", booking.id)
        return {"success": False, "error": "Invalid external service response"}
