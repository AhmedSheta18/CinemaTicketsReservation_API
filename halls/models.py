from django.db import models
from django.utils.text import slugify

# Create your models here.
class Hall(models.Model):
    name = models.CharField(max_length=50, unique=True)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if not self.slug:
            self.slug = slugify(self.name + '_' + str(self.id))
            super().save(*args, **kwargs)

        # check is a new hall
        if not self.pk:
            # Create seats for the new hall 
            seats_to_create = []
            for i in range(1, self.capacity + 1):
                first_char = self.name.replace(' ','')[0:2].upper()
                if len(first_char) < 2: 
                    first_char += 'X'
                seat_name= f"{first_char}-{i}"
                # Create a seat with the formatted number
                seats_to_create.append(
                    Seats(
                        hall=self, 
                        seat_number=seat_name,
                        is_available=True
                    )
                )
                Seats.objects.bulk_create(seats_to_create)

    def __str__(self):
        return self.name
    

class Seats(models.Model):
    hall = models.ForeignKey('hall', related_name='hall_seats', on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10 , null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hall.name} - Seat {self.seat_number}"
    
    
    class Meta:
        unique_together = ('hall', 'seat_number')