from django.contrib import admin
from .models import Movie, Review, Catogory  # Changed Movies to Movie

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Catogory)
