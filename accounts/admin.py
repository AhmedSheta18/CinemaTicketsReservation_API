from django.contrib import admin

# Register your models here.
from .models import Profile, Auther
admin.site.register(Auther)
admin.site.register(Profile)
