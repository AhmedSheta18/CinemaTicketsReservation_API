from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from halls.models import Hall, Seats



# Create your models here.
class Ticket(models.Model):
    user = models.ForeignKey(User, related_name='user_tickets', on_delete=models.CASCADE)
    screening = models.ForeignKey('movies.Screening', related_name='screening_tickets', on_delete=models.CASCADE)
    seat = models.ForeignKey('halls.Seats', related_name='seat_tickets', on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        
        if not self.seat.is_available:
            raise ValueError("The selected seat is not available.")
        self.seat.is_available = False
        self.seat.save()

        # or 
        # if not self.pk:
        #     self.seat.is_available = False
        #     self.seat.save()

        super().save(*args, **kwargs) # Call the real save() method

    def __str__(self):
        return f"Ticket for {self.user.username} - {self.screening.movie.title} at {self.screening.start_time.strftime('%Y-%m-%d %H:%M')} - Seat: {self.seat.seat_number}" 
    
    class Meta:
        unique_together = ('screening', 'seat')