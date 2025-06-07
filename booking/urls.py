from django.urls import path
from .views import list_classes, book_class, get_bookings_by_email,add_class

urlpatterns = [
    path('classes/add/', add_class),
    path('classes/', list_classes),
    path('book/', book_class),
    path('bookings/', get_bookings_by_email),
]
