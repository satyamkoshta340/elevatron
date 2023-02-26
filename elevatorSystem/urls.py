from django.urls import path

from elevatorSystem import views

urlpatterns = [
    path( '', views.createElevatorSystem, name='index'), # Initialise the elevator system to create ‘n’ elevators in the system
    path( '<int:elevator_system_id>/floor/<int:requested_floor>/', views.makeElevatorSystemRequest), # Saves user request to the list of requests for a elevator
    path( 'elevator/<int:elevator_id>/', views.getElevator),
    path( 'elevator/<int:elevator_id>/requests', views.getElevatorRequests), # Fetch all requests for a given elevator
    path( 'elevator/<int:elevator_id>/nextdestination', views.getNextDestinationOfElevator), # Fetch the next destination floor for a given elevator
    path( 'elevator/<int:elevator_id>/motionstatus/', views.getMotionStatusOfElevator ), # Fetch if the elevator is moving up or down currently
    path( 'elevator/<int:elevator_id>/workingstatus/', views.setElevatorWorkingStatus ), # Mark a elevator as not working or in maintenance 
    path( 'elevator/<int:elevator_id>/door', views.setElevatorDoor), # Open/close the door.
]
