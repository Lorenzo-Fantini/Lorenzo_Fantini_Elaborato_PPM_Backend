import requests
from getpass import getpass
import json

server_url= "http://localhost:8000/"

def help():
	print(
		"\n help: prints this help message \n\n",
		"register_user: starts new user registration process \n\n",
		"delete_user: deletes existing user account \n\n",
		"login: logs you in with the credentials of a registered user\n\n",
		"logout: logs you out\n\n",
		"list_events: lists available events \n\n",
		"get_event_details: prints the details of a specific event \n\n",
		"create_event (admin only): allows you to create a new event \n\n",
		"delete_event (admin only): allows you to delete a specific event \n\n",
		"list_reservations (authenticated users only): allows you to list all your reservations \n\n",
		"create_reservation (authenticated users only): allows you to create a new reservation \n\n",
		"update_reservation (authenticated users only): allows you to change the number of tickets "
		"of a reservation \n\n",
		"delete_reservation (authenticated users only): allows you to delete a reservation \n"
	)

def register_user():
	username = input("Enter username: ")
	email = input("Enter email: ")
	password = getpass("Enter password: ")
	confirm_password = getpass("Confirm password: ")
	age= input("Enter age: ")
	budget= input("Enter budget: ")

	if password != confirm_password:
		print("Error: Passwords do not match!")
		return

	# Prepare the data payload
	data = {
        "username": username,
        "email": email,
        "password": password,
        "age": age,
        "budget": budget
    }

	# Configure the URL for your registration endpoint
	url = server_url + "account/register/"

	# Send a POST request with JSON payload
	try:
		response = requests.post(url, json=data)
		if response.status_code == 201:
			print("Registration successful!")
		else:
			# If you receive an error, print out the details
			errors = response.json()
			print("Registration failed:")
			for field, messages in errors.items():
				print(f"{field}: {messages}")
	except requests.RequestException as e:
		print("Error connecting to the API:", e)
	
def delete_user(auth_token_var):
	if auth_token_var is not None:
		url= server_url + "account/delete/"
		headers = {
			"Authorization": f"Token {auth_token_var}"
		}
		choice= input("are you sure you want to delete your account? (y/n): ")
		if choice=="y":
			response= requests.delete(url, headers=headers)
			if response.status_code == 204:
				print("deletion successful\n")
			else:
				print("deletion failed\n")
		else:
			print("deletion cancelled\n")
	else:
		print("you are not logged in")
		
def login(auth_token_var):
	if auth_token_var is not None:
		print("you are already logged in")
	else:
		url= server_url + "account/token/"
		username= input("\nenter your username: ")
		password= getpass("\nenter your password: ")
		data= {
			"username": username,
			"password": password
		}
		response= requests.post(url, json=data)

		if response.status_code == 200:
			print("\nlogin successful\n")
			auth_token_var= response.json()["token"]
		else:
			print("login failed\n")

	return auth_token_var

def logout(auth_token_var):
	if auth_token_var is None:
		print("\nyou are not logged in\n")
	else:
		print("\nlogged out\n")

	return None
	
def list_events():
	url= server_url + "events/list/"
	response= requests.get(url)
	
	print("\navailable events:\n")
	for event in response.json():
		print(event)
		print("\n")

def get_event_details():
	event= input("what event would you like to know more about? (type event title): ")
	url= server_url + "events/detail/" + event + "/"
	response= requests.get(url)

	print(response.json())

def create_event(admin_auth_token):
	url= server_url + "events/create/"

	title= input("enter event title: ")
	description= input("enter event description: ")
	location= input("enter event location: ")
	date_and_time= input("please enter the date and time of the event (in json format): ")
	ticket_price= input("please enter the ticket price: ")
	available_tickets= input("please enter the number of tickets: ")
	age= input("pleaser enter the event age (0/14/18): ")

	data= {
		"title": title,
		"description": description,
		"location": location,
		"date_and_time": date_and_time,
		"ticket_price": ticket_price,
		"available_tickets": available_tickets,
		"age": age
	}

	headers= {
		"Authorization": f"Token {admin_auth_token}"
	}

	try:
		response = requests.post(url, json=data, headers=headers)
		if response.status_code == 201:
			print("creation successful")
		else:
			# If you receive an error, print out the details
			errors = response.json()
			print("creation failed:")
			for field, messages in errors.items():
				print(f"{field}: {messages}")
	except requests.RequestException as e:
		print("Error connecting to the API:", e)

def delete_event(admin_auth_token):
	event= input("insert title of event to delete: ")
	url= server_url + "events/delete/" + event + "/"

	headers = {
		"Authorization": f"Token {admin_auth_token}"
	}

	try:
		response = requests.delete(url, headers=headers)
		if response.status_code == 204:
			print("deletion successful")
		else:
			# If you receive an error, print out the details
			errors = response.json()
			print("deletion failed")
			for field, messages in errors.items():
				print(f"{field}: {messages}")
	except requests.RequestException as e:
		print("Error connecting to the API:", e)

def list_reservations(auth_token_var):
	url= server_url + "reservations/list/"

	headers = {
		"Authorization": f"Token {auth_token_var}"
	}

	response = requests.get(url, headers=headers)

	print("\ncurrent reservations:\n")
	for reservation in response.json():
		print(reservation)
		print("\n")

def create_reservation(auth_token_var):
	url= server_url + "reservations/create/"

	event= input("\nenter the name of the event you want to buy tickets for: ")
	num_tickets= input("\nenter the number of tickets you want to buy: ")

	data= {
		"event": event,
		"num_tickets": num_tickets
	}

	headers = {
		"Authorization": f"Token {auth_token_var}"
	}

	try:
		response = requests.post(url, json=data, headers=headers)
		if response.status_code == 201:
			print("reservation created successfully")
		else:
			# If you receive an error, print out the details
			errors = response.json()
			print("reservation creation failed:")
			for field, messages in errors.items():
				print(f"{field}: {messages}")
	except requests.RequestException as e:
		print("Error connecting to the API:", e)

if __name__ == '__main__':
	current_action = "default"
	auth_token = None
	while(current_action != "quit"):
		current_action = input("please specify an action (type help for more information about "
							   "available actions): ")
		match current_action:
			case "register_user":
				register_user()
			case "delete_user":
				delete_user(auth_token)
			case "help":
				help()
			case "login":
				auth_token= login(auth_token)
			case "logout":
				auth_token= logout(auth_token)
			case "list_events":
				list_events()
			case "get_event_details":
				get_event_details()
			case "create_event":
				create_event(auth_token)
			case "delete_event":
				delete_event(auth_token)
			case "list_reservations":
				list_reservations(auth_token)
			case "create_reservation":
				create_reservation(auth_token)
			case _:
				if current_action != "quit":
					print("invalid command (type help to list available actions)")