from datetime import timedelta
from django.db import models
from django.utils.text import slugify
from halls.models import Hall, Seats
from django.contrib.auth.models import User

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=100, default='Unknown')
    description = models.TextField()
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    genres = models.ManyToManyField('catogory', related_name='catogories_movies', blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self,*args , **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + '_' + str(self.id))
        super().save(*args, **kwargs)

    

    def __str__(self):
        return self.title
    
    def get_average_rating(self):
        reviews = self.movie_reviews.all()
        if not reviews:
            return None
        total_rating = sum(review.rating for review in reviews)
        return total_rating / len(reviews)

class Review(models.Model):
    movies = models.ForeignKey(Movie, related_name='moviess_reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
    

class Catogory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    


class Screening(models.Model):
    movies = models.ForeignKey('Movie', related_name='screenings', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    brack_time = models.TimeField(verbose_name='brack time by minutes', default='00:15')
    hall = models.ForeignKey('halls.Hall', related_name='screenings', on_delete=models.CASCADE)
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return f"{self.movie.title} - {self.screening_time.strftime('%Y-%m-%d %H:%M')}"
    
    def get_end_time(self):
        duration = self.movies.duration
        return self.start_time + timedelta(minutes=duration) + timedelta(minutes=self.brack_time.minute)
    
    def get_available_seats(self):
        all_seats = self.hall.hall_seats.all()

        booked_seats = Seats.objects.filter(
            tickets__screening=self
        )
        return all_seats.exclude(id__in=booked_seats.values_list('id', flat=True))
    
    
    # def get_absolute_url(self):
    #     from django.urls import reverse
    #     return reverse('movies:screening_detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['start_time']


