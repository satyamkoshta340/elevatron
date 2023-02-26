from django.contrib import admin
from .models import ElevatorSystem, Elevator, ElevatorSystemRequest

# Register your models here.
@admin.register(ElevatorSystem, Elevator, ElevatorSystemRequest)
class AuthorAdmin( admin.ModelAdmin ):
    pass