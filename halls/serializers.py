from rest_framework import serializers
from .models import Hall, Seats 

class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ['id', 'name', 'capacity', 'is_active', 'location']
        read_only_fields = ['id']

class SeatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seats
        fields = ['id', 'hall', 'seat_number', 'is_available']
        read_only_fields = ['id']

    def validate_seat_number(self, value):
        if not value:
            raise serializers.ValidationError("Seat number cannot be empty.")
        return value

    def validate_hall(self, value):
        if not value.is_active:
            raise serializers.ValidationError("Cannot assign seats to an inactive hall.")
        return value