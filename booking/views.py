import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer
from django.utils import timezone

logger = logging.getLogger('booking')

@api_view(['POST'])
def add_class(request):
    serializer = FitnessClassSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        logger.info(f"Class added: {instance.name} by {instance.instructor} at {instance.datetime}")
        return Response(serializer.data, status=201)
    logger.warning(f"Failed to add class. Errors: {serializer.errors}")
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def list_classes(request):
    classes = FitnessClass.objects.filter(datetime__gte=timezone.now())
    serializer = FitnessClassSerializer(classes, many=True)
    logger.info(f"Listed {len(serializer.data)} upcoming classes")
    return Response(serializer.data)

@api_view(['POST'])
def book_class(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        booking = serializer.save()
        logger.info(f"Booking successful for {booking.client_email} - Class: {booking.fitness_class}")
        return Response({"message": "Booking successful."}, status=201)
    logger.warning(f"Booking failed - Data: {request.data} - Errors: {serializer.errors}")
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def get_bookings_by_email(request):
    email = request.query_params.get("email")

    if not email:
        logger.warning("Booking lookup failed: Missing email parameter.")
        return Response({"error": "Email parameter is required"}, status=400)

    bookings = Booking.objects.filter(client_email=email)

    logger.info(f"Fetched {bookings.count()} bookings for email: {email}")

    return Response([
        {
            "id": b.id,
            "class": str(b.fitness_class),
            "client_name": b.client_name
        } for b in bookings
    ])
