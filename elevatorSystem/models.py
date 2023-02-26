from django.db import models
from django.utils import timezone
from django.core.validators import  MinValueValidator 
# Create your models here.
class ElevatorSystem( models.Model ):
    no_of_floors = models.PositiveIntegerField( validators=[MinValueValidator(1)] )
    no_of_elevators = models.PositiveIntegerField( validators=[MinValueValidator(1)] )
    name = models.CharField( max_length=50 )
    created_at = models.DateTimeField( default= timezone.now )

class Elevator( models.Model ):
    MAINTENANCE = "maintenance"
    NOT_WORKING = "not working"
    WORKING = "working"
    OPEN = "open"
    CLOSE = "close"
    UP = "moving up"
    DOWN = "moving down"
    WAITING = "waiting"
    IDLE = "idle"
    ELEVATOR_WORKING_STATUS_CHOICES = [
        (MAINTENANCE, "maintenance"),
        (NOT_WORKING, "not working"),
        (WORKING, "working")
    ]
    ELEVATOR_DOOR_STATUS_CHOICES = [
        (OPEN, "open"),
        (CLOSE, "close")
    ]
    ELEVATOR_MOTION_STATUS_CHOICES = [
        (UP, "moving up"),
        (DOWN, "moving down"),
        (WAITING, "waiting"),
        (IDLE, "idle")
    ]
    elevator_system = models.ForeignKey(ElevatorSystem, on_delete=models.CASCADE )
    current_floor = models.PositiveIntegerField(default=0)
    working_status = models.CharField(
        max_length= 15,
        choices= ELEVATOR_WORKING_STATUS_CHOICES,
        default= WORKING,
    )
    door_status = models.CharField(
        max_length=5,
        choices= ELEVATOR_DOOR_STATUS_CHOICES,
        default= CLOSE
    )
    motion_status = models.CharField(
        max_length=11,
        choices= ELEVATOR_MOTION_STATUS_CHOICES,
        default= IDLE
    )
    next_destination_floor = models.IntegerField( default=None, null=True )
    last_service_date = models.DateTimeField(default= timezone.now )

class ElevatorSystemRequest( models.Model ):
    OPEN = "open"
    CLOSE = "close"
    REQUEST_STATUS_CHOICES = [
        (OPEN,"open"),
        (CLOSE, "close")
    ]
    elevator_system = models.ForeignKey(ElevatorSystem, on_delete=models.DO_NOTHING )
    elevator = models.ForeignKey(Elevator, on_delete=models.DO_NOTHING, null=False)
    requested_floor = models.IntegerField()
    request_status = models.CharField(
        max_length=5,
        choices= REQUEST_STATUS_CHOICES,
        default= OPEN
    )
    reqyested_at = models.DateTimeField( default=timezone.now)
