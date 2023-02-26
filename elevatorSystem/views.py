from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import ElevatorSystem, Elevator, ElevatorSystemRequest
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import sys

# Create your views here.
def index( request ):
    return HttpResponse("This is the Elevator System")

@csrf_exempt
def createElevatorSystem( request ):
    if request.method == "GET":
        elevator_systems = list(ElevatorSystem.objects.all())
        elevator_systems = map( lambda x: model_to_dict(x), elevator_systems)
        return JsonResponse({"message":"This is the list of working systems",
        'elevator_systems': list(elevator_systems) })
    elif request.method == "POST":
        print(request.POST)
        try:
            name = request.POST['name']
            no_of_elevators = int(request.POST['no_of_elevators'])
            no_of_floors = int(request.POST['no_of_floors'])
        except:
            return JsonResponse( { 'message': "Please provide required body fields"}, status=400)
        try:
            elevator_system = ElevatorSystem( no_of_elevators=no_of_elevators,
                no_of_floors = no_of_floors,
                name = name
                )
        except:
            return JsonResponse({ 'message': sys.exc_info()[0]}, status=400 )

        elevator_system.save()
        list_of_elevators = []
        for i in range( no_of_elevators ):
            elevator = Elevator(elevator_system = elevator_system)
            elevator.save()
            list_of_elevators.append(model_to_dict(elevator))
        return JsonResponse({
            'elevator_system': model_to_dict(elevator_system),
            'list_of_elevators': list_of_elevators
        })
    else:
        return JsonResponse({ 'message': "can't find the path" }, status=404)

@csrf_exempt
def getElevator(request, elevator_id):
    if request.method == "GET":
        elevator = Elevator.objects.filter(pk=elevator_id).values()[0]
        return JsonResponse( { "elevator": elevator } )

@csrf_exempt
def setElevatorWorkingStatus(request, elevator_id):
    if( request.method =="POST" ):
        working_status = request.POST["working_status"]
        
        modified_elevator_count = Elevator.objects.filter(pk=elevator_id).update(working_status= working_status)
        if modified_elevator_count == 0:
            return JsonResponse({ 'message': "can't find the elevator with given id" }, status=404)
        
        modified_elevator = Elevator.objects.filter(pk=elevator_id).values()[0]
        
        return JsonResponse( { 
            "modified_elevator_count": modified_elevator_count,
            "modified_elevator": modified_elevator})

@csrf_exempt
def getMotionStatusOfElevator(request, elevator_id):
    if request.method == "GET":
        elevator = Elevator.objects.filter(pk=elevator_id).values()[0]
        return JsonResponse( { 
            "motion status": elevator.motion_status,
            "elevator": elevator})

@csrf_exempt
def setElevatorDoor(request, elevator_id):
    if request.method == "POST":
        door_status = request.POST["door_status"]
        if door_status not in ["open", "close"]:
            return JsonResponse({ 'message': "invalid door operation, valid operations are 'open', 'close'." }, status=400)

        try:
            elevator = Elevator.objects.filter(pk = elevator_id).values()[0]
        except:
            return JsonResponse({ 'message': "can't find the elevator with given id" }, status=404)

        if elevator["motion_status"] in ["idle", "waiting"]:
            elevator["door_status"] = door_status
            Elevator.objects.filter(pk = elevator_id).update( door_status = door_status)
            return JsonResponse( {"elevator": elevator})
        else:
            return JsonResponse({ 'message': "can't operate door operation on moving elevator" }, status=400)


@csrf_exempt
def makeElevatorSystemRequest(request, elevator_system_id, requested_floor):
    if request.method == "GET":
        try:
            elevator_system_instance = ElevatorSystem.objects.filter(pk = elevator_system_id)
            elevator_system = elevator_system_instance.values()[0]
            elevator_system_instance = elevator_system_instance.get()
        except:
            return JsonResponse({ 'message': "can't find the elevator system with given id" }, status=404)

        if requested_floor < 0:
            return JsonResponse({ 'message': "floor number can't be negative" }, status=400)
        elif requested_floor > elevator_system["no_of_floors"]:
            return JsonResponse({ 'message': "can't request for floor number greater than the height of elevator system!"}, status=400)

        
        elevators = Elevator.objects.filter(elevator_system=elevator_system_instance, motion_status="idle")

        if len(elevators) == 0:
            return JsonResponse({ "message": "please request again" })
        
        """ Select the optimal elevator here """
        selected_elevator = min( elevators, key = lambda x: abs(model_to_dict(x)["current_floor"] - requested_floor) )
        # selected_elevator = elevators[0]

        floor_request = ElevatorSystemRequest(elevator_system=elevator_system_instance, requested_floor=requested_floor, elevator = selected_elevator)
        floor_request.save()

        selected_elevator = model_to_dict(selected_elevator)
        # print(selected_elevator)
        # print("=============================\n")
        selected_elevator["next_destination_floor"] = requested_floor
        if requested_floor > selected_elevator["current_floor"]:
            selected_elevator["motion_status"]="moving up"
        else:
            selected_elevator["motion_status"] = "moving down"
        
        Elevator.objects.filter(pk=selected_elevator["id"]).update(
            current_floor = selected_elevator["current_floor"],
            next_destination_floor = selected_elevator["next_destination_floor"],
            motion_status= selected_elevator["motion_status"]
        )

        """ assuming elevator reaches destination floor in the mean time """
        selected_elevator["current_floor"] = requested_floor
        selected_elevator["next_destination_floor"] = None
        selected_elevator["motion_status"] = "idle"

        Elevator.objects.filter(pk=selected_elevator["id"]).update(
            current_floor = selected_elevator["current_floor"],
            next_destination_floor = selected_elevator["next_destination_floor"],
            motion_status= selected_elevator["motion_status"]
        )

        return JsonResponse({ "message": "selected elevator is with id {id}".format(id= selected_elevator["id"])})


@csrf_exempt
def getElevatorRequests(request, elevator_id):

    try:
        elevator = Elevator.objects.filter(pk=elevator_id).get()
    except:
        return JsonResponse({ 'message': "can't find the elevator with given id" }, status=404)
    
    elevator_requests = ElevatorSystemRequest.objects.filter(elevator=elevator)

    print("========================\n")
    print(elevator_requests)
    elevator_requests = map( lambda x: model_to_dict(x), elevator_requests)
    return JsonResponse({ 
        "message": "success",
        "list_of requests": list(elevator_requests)
    })

@csrf_exempt
def getNextDestinationOfElevator(request, elevator_id):
    try:
        elevator = Elevator.objects.filter(pk=elevator_id).values()[0]
    except:
        return JsonResponse({ 'message': "can't find the elevator with given id" }, status=404)

    return JsonResponse({
        "message": "next destination of the elevator is {dest}".format(dest=elevator["next_destination_floor"])
    })