from rest_framework import serializers
from .models import FitnessClass, Booking

class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'datetime', 'instructor', 'available_slots']

class BookingSerializer(serializers.ModelSerializer):
    class_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'class_id', 'client_name', 'client_email']

    def validate(self, data):
        from .models import FitnessClass
        try:
            cls = FitnessClass.objects.get(id=data['class_id'])
        except FitnessClass.DoesNotExist:
            raise serializers.ValidationError("Class not found.")

        if cls.available_slots <= 0:
            raise serializers.ValidationError("No available slots.")

        data['fitness_class'] = cls
        return data

    def create(self, validated_data):
        # Remove class_id from validated_data before creating Booking
        validated_data.pop('class_id', None)
        cls = validated_data.pop('fitness_class')
        cls.available_slots -= 1
        cls.save()
        return Booking.objects.create(fitness_class=cls, **validated_data)
