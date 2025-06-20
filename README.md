# Event reservation system

This project is a Django-based web application that provides a RESTful API for managing users, events, and reservations. Users can register, manage their profiles, and book reservations for various events. If you use the client for the first time the api might take a bit to respond due to Render's deploy offer.

## Key features

* User registration, authentication and deletion
* Event creation, listing, and details views
* Reservation creation, updating, and cancellation with ticket availability management
* Budget tracking for users
* Admin functionality for managing events and listing transactions
* Command-line client for interacting with the API

## How to use the client

Python is required in order to use the client. Using the client is pretty straightforward, simply download it and run it with python. All available actions and their functionality can be listed by typing "help".

## Available actions

* help: prints all available actions and their functionality
* register_user: allows an anonymous users to create a new account
* delete_user: allows an authenticated user to delete their account
* login: allows an anonymous user to log in by providing account credentials
* logout: allows an authenticated user to log out
* list_events: lists available events
* get_event_details: prints the all details about a specific event
* create_event: allows the admin to create a new event
* delete_event: allows the admin to delete an existing event
* list_transactions: allows the admin to list all the occurred transactions
* list_reservations: allows an authenticated user to list all their reservations
* create_reservation: allows an authenticated user to create a new reservation for an event (it's not possible to create more than a single reservation per event)
* update_reservation: allows an authenticated user to update  the number of tickets of an existing reservation
* delete_reservation: allows an authenticated user to delete an existing reservation
* quit: quit the client

## Admin credentials

* username: admin
* password: admin
