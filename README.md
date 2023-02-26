# elevatron
Elevator simulation python backend


## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/satyamkoshta340/elevatron.git
$ cd elevatron
```

Then install the dependencies:

```sh
$ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:
```sh
$ python manage.py runserver
```

## APIs entertained by the project
    > Initialise the elevator system to create ‘n’ elevators in the system
    * http://127.0.0.1:8000/elevatorsystem
    * method: POST
    * body: form-data
    *   {
            name: "Pyramid Homes Elevator System",
            no_of_floors: 11,
            no_of_elevators: 4
        }

    > Saves user request to the list of requests for a elevator
    * http://127.0.0.1:8000/elevatorsystem/<int:elevator_system_id>/floor/<int:requested_floor>/
    * method: get
    * working: selects optimum elevator from available elevators in the system and assign it the task

    > Get perticular elevator details
    * http://127.0.0.1:8000/elevatorsystem/elevator/<int:elevator_id>/
    * method: get

    > Fetch all requests for a given elevator
    * http://127.0.0.1:8000/elevatorsystem/elevator/<int:elevator_id>/requests
    * method: get

    > Fetch the next destination floor for a given elevator
    * http://127.0.0.1:8000/elevatorsystem/elevator/<int:elevator_id>/nextdestination
    * method: get

    > Fetch if the elevator is moving up or down currently
    * http://127.0.0.1:8000/elevatorsystem/elevator/<int:elevator_id>/motionstatus/
    * method: get

    > Mark a elevator as not working or in maintenance 
    * http://127.0.0.1:8000/elevatorsystem/elevator/<int:elevator_id>/workingstatus/
    * method: POST
    * body: form-data
    *   {
            working_status: "working"
        }

    > Open/close the door.
    * http://127.0.0.1:8000/elevatorsystem/elevator/<int:elevator_id>/door
    * method: POST
    * body: form-data
    *   {
            door_status: "close"
        }
