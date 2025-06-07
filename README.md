# 🧘‍♀️ Fitness Studio Booking API

A simple Django REST API for managing fitness class schedules and client bookings. It supports class listings, bookings, and querying bookings by email.

---

## 📁 Project Structure

fitness_booking/
├── booking/             # App for fitness classes and bookings  
│   ├── models.py  
│   ├── views.py  
│   ├── serializers.py  
│   ├── urls.py  
├── fitness_booking/  
│   ├── settings.py  
│   ├── urls.py  
├── manage.py  
├── db.sqlite3  

---

## 🚀 Setup Instructions

### 1. Clone the Repository
``` git clone https://github.com/yourusername/fitness-booking-api.git
cd fitness-booking-api

### 2. Create a Virtual Environment
python -m venv env  
source env/bin/activate      # On Windows: env\Scripts\activate  

### 3. Install Dependencies
pip install -r requirements.txt  

(If no `requirements.txt`, install manually:)  
pip install django djangorestframework pytz  

### 4. Run Migrations
python manage.py migrate  

### 5. Create Superuser (Optional)
python manage.py createsuperuser  

### 6. Run the Server
python manage.py runserver  

Visit: http://127.0.0.1:8000/

---

## 🔗 API Endpoints

### 1. List All Upcoming Classes
GET /classes/

Sample cURL:
curl -X GET http://127.0.0.1:8000/classes/

Sample Response:
[
  {
    "id": 1,
    "name": "Yoga",
    "datetime": "2025-06-08T07:00:00+05:30",
    "instructor": "Asha",
    "available_slots": 5
  }
]

---

### 2. Add a New Fitness Class
POST /classes/add/

Sample JSON Body:
{
  "name": "Zumba",
  "datetime": "2025-06-09T09:00:00",
  "instructor": "Ravi",
  "available_slots": 10
}

Sample cURL:
curl -X POST http://127.0.0.1:8000/classes/add/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Zumba","datetime":"2025-06-09T09:00:00","instructor":"Ravi","available_slots":10}'

---

### 3. Book a Class
POST /book/

Sample JSON Body:
{
  "class_id": 1,
  "client_name": "John Doe",
  "client_email": "john@example.com"
}

Sample cURL:
curl -X POST http://127.0.0.1:8000/book/ \
  -H "Content-Type: application/json" \
  -d '{"class_id":1,"client_name":"John Doe","client_email":"john@example.com"}'

Sample Success Response:
{
  "message": "Booking successful."
}

Error Response (No slots left):
{
  "non_field_errors": ["No available slots."]
}

---

### 4. Get Bookings by Email
GET /bookings/?email=john@example.com

Sample cURL:
curl -X GET "http://127.0.0.1:8000/bookings/?email=john@example.com"

Sample Response:
[
  {
    "id": 1,
    "class": "Yoga on June 8, 2025, 7:00 AM",
    "client_name": "John Doe"
  }
]

---

## 📝 Logs

All API activity is logged to `booking.log`, including:
- Class creation
- Booking attempts and errors
- Email-based booking lookups

---

## 🧪 Run Unit Tests
python manage.py test booking

---

## 🕒 Timezone Management

All class datetimes are stored in IST (Asia/Kolkata). Django handles automatic conversion if clients use different timezones.

---

