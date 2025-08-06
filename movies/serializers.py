from rest_framework import serializers
from .models import Movies, Review, Catogory , Screening

class MoviesSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movies
        fields = ['id', 'title', 'director', 'description', 'release_date', 'duration', 'rating', 'genres', 'average_rating']
        read_only_fields = ['id']

    def get_average_rating(self, obj):
        return obj.get_average_rating()
    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'movies', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']

class CatogorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Catogory
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']

class ScreeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screening
        fields = ['id', 'movies', 'start_time', 'brack_time', 'hall', 'ticket_price']
        read_only_fields = ['id']

    def validate(self, data):
        if data['start_time'] < data['movies'].release_date:
            raise serializers.ValidationError("Screening start time cannot be before the movie's release date.")
        return data
    
    def validate_hall(self, value):
        if not value.is_active:
            raise serializers.ValidationError("Cannot schedule screenings in an inactive hall.")
        return value
    
    def validate_ticket_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Ticket price must be a positive number.")
        return value


