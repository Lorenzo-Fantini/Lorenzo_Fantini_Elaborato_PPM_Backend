import requests
from getpass import getpass
import json

server_url= "https://lorenzo-fantini-elaborato-ppm-backend.onrender.com/"

def help():
	print(
		"\n help: prints this help message \n\n",
		"register_user: starts new user registration process \n\n",
		"delete_user (authenticated users only): deletes existing user account \n\n",
		"login: logs you in with the credentials of a registered user\n\n",
		"logout: logs you out\n\n",
		"list_events: lists available events \n\n",
		"get_event_details: prints the details of a specific event \n\n",
		"create_event (admin only): allows you to create a new event \n\n",
		"delete_event (admin only): allows you to delete a specific event \n\n",
		"list_transactions (admin only): allows you to list all transactions \n\n",
		"list_reservations (authenticated users only): allows you to list all your reservations \n\n",
		"create_reservation (authenticated users only): allows you to create a new reservation \n\n",
		"update_reservation (authenticated users only): allows you to change the number of tickets "
		"of a reservation \n\n",
		"delete_reservation (authenticated users only): allows you to delete a reservation \n\n",
		"quit: exit the client\n"
	)

def register_user():
	username = input("\nEnter username: ")
	email = input("\nEnter email: ")
	password = getpass("\nEnter password: ")
	confirm_password = getpass("\nConfirm password: ")
	age= input("\nEnter age: ")
	budget= input("\nEnter budget: ")

	if password != confirm_password:
		print("\nError: Passwords do not match!")
		return

	data = {
        "username": username,
        "email": email,
        "password": password,
        "age": age,
        "budget": budget
    }

	url = server_url + "account/register/"

	try:
		response = requests.post(url, json=data)
		if response.status_code == 201:
			print("\nRegistration successful\n")
		else:
			errors = response.json()
			print("\nRegistration failed:")
			for field, messages in errors.items():
				print(f"{field}: {messages}")
	except requests.RequestException as e:
		print("\nError connecting to the API:", e)
	
def delete_user(auth_token_var):
	if auth_token_var is not None:

		url= server_url + "account/delete/"

		headers = {
			"Authorization": f"Token {auth_token_var}"
		}

		choice= input("\nAre you sure you want to delete your account? (y/n): ")
		if choice=="y":
			response= requests.delete(url, headers=headers)
			if response.status_code == 204:
				print("\nDeletion successful\n")
				auth_token_var= None
			else:
				print("\nDeletion failed\n")
		else:
			print("\nDeletion cancelled\n")
	else:
		print("\nYou are not logged in\n")

	return auth_token_var
		
def login(auth_token_var):
	if auth_token_var is not None:
		print("\nYou are already logged in\n")
	else:
		url= server_url + "account/token/"
		username= input("\nEnter your username: ")
		password= getpass("\nEnter your password: ")
		data= {
			"username": username,
			"password": password
		}
		response= requests.post(url, json=data)

		if response.status_code == 200:
			print("\nLogin successful\n")
			auth_token_var= response.json()["token"]
		else:
			print("\nLogin failed\n")

	return auth_token_var

def logout(auth_token_var):
	if auth_token_var is None:
		print("\nYou are not logged in\n")
	else:
		print("\nLogged out\n")

	return None
	
def list_events():
	url= server_url + "events/list/"
	
	response= requests.get(url)
	
	print("\nAvailable events:\n")
	for event in response.json():
		print(event)
		print("\n")

def get_event_details():
	event= input("\nWhat event would you like to know more about? (type event title): ")

	url= server_url + "events/detail/" + event + "/"

	response= requests.get(url)

	print("\n")
	print(response.json())

def create_event(admin_auth_token):
	if admin_auth_token is None:
		print("\nYou are not logged in\n")
	else:
		url= server_url + "events/create/"

		title= input("\nEnter event title: ")
		description= input("\nEnter event description: ")
		location= input("\nEnter event location: ")
		date_and_time= input("\nEnter the date and time of the event (in json format): ")
		ticket_price= input("\nEnter the ticket price: ")
		available_tickets= input("\nEnter the number of tickets: ")
		age= input("\nEnter the event age (0/14/18): ")

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
				print("\nCreation successful")
			else:
				errors = response.json()
				print("\nCreation failed:")
				for field, messages in errors.items():
					print(f"{field}: {messages}")
		except requests.RequestException as e:
			print("\nError connecting to the API:", e)

def delete_event(admin_auth_token):
	if admin_auth_token is None:
		print("\nYou are not logged in\n")
	else:
		event= input("\nInsert title of event to delete: ")

		url= server_url + "events/delete/" + event + "/"

		headers = {
			"Authorization": f"Token {admin_auth_token}"
		}

		try:
			response = requests.delete(url, headers=headers)
			if response.status_code == 204:
				print("\nDeletion successful")
			else:
				errors = response.json()
				print("\nDeletion failed")
				for field, messages in errors.items():
					print(f"{field}: {messages}")
		except requests.RequestException as e:
			print("\nError connecting to the API:", e)

def list_transactions(admin_auth_token):
	if admin_auth_token is None:
		print("\nYou are not logged in\n")
	else:
		url= server_url + "transactions/list/"

		headers = {
			"Authorization": f"Token {admin_auth_token}"
		}

		try:
			response = requests.get(url, headers=headers)
			if response.status_code == 200:
				print("\nTransactions:\n")
				for reservation in response.json():
					print(reservation)
					print("\n")
			else:
				errors = response.json()
				print("\nAn error occurred while fetching transactions data:")
				for field, messages in errors.items():
					print(f"{field}: {messages}")
		except requests.RequestException as e:
			print("\nError connecting to the API:", e)

def list_reservations(auth_token_var):
	if auth_token_var is None:
		print("\nYou are not logged in\n")
	else:
		url= server_url + "reservations/list/"

		headers = {
			"Authorization": f"Token {auth_token_var}"
		}

		try:
			response = requests.get(url, headers=headers)
			if response.status_code == 200:
				print("\nCurrent reservations:\n")
				for reservation in response.json():
					print(reservation)
					print("\n")
			else:
				errors = response.json()
				print("\nAn error occurred while fetching reservations data:")
				for field, messages in errors.items():
					print(f"{field}: {messages}")
		except requests.RequestException as e:
			print("\nError connecting to the API:", e)

def create_reservation(auth_token_var):
	if auth_token_var is None:
		print("\nYou are not logged in\n")
	else:
		url= server_url + "reservations/create/"

		event= input("\nEnter the name of the event you want to buy tickets for: ")
		num_tickets= input("\nEnter the number of tickets you want to buy: ")

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
				print("\nReservation created successfully")
			else:
				errors = response.json()
				print("\nReservation creation failed:")
				for field, messages in errors.items():
					print(f"{field}: {messages}")
		except requests.RequestException as e:
			print("\nError connecting to the API:", e)

def update_reservation(auth_token_var):
	if auth_token_var is None:
		print("\nYou are not logged in\n")
	else:
		reservation= input("\nEnter the title of the event of the reservation you want to update: ")
		new_tickets_num= input("\nEnter the new number of tickets: ")

		url= server_url + "reservations/update/" + reservation + "/"

		data= {
			"reservation": reservation,
			"num_tickets": new_tickets_num
		}

		headers = {
			"Authorization": f"Token {auth_token_var}"
		}

		try:
			response = requests.patch(url, json=data, headers=headers)
			if response.status_code == 200:
				print("\nReservation updated successfully")
			else:
				errors = response.json()
				print("\nReservation update failed:")
				for field, messages in errors.items():
					print(f"{field}: {messages}")
		except requests.RequestException as e:
			print("\nError connecting to the API:", e)

def delete_reservation(auth_token_var):
	if auth_token_var is None:
		print("\nYou are not logged in\n")
	else:
		reservation = input("\nEnter the title of the event of the reservation you want to delete: ")

		url= server_url + "reservations/delete/" + reservation + "/"

		data= {
			"reservation": reservation
		}

		headers = {
			"Authorization": f"Token {auth_token_var}"
		}

		try:
			response = requests.delete(url, json=data, headers=headers)
			if response.status_code == 204:
				print("\nReservation deleted successfully")
			else:
				errors = response.json()
				print("\nReservation deletion failed:")
				for field, messages in errors.items():
					print(f"{field}: {messages}")
		except requests.RequestException as e:
			print("\nError connecting to the API:", e)

if __name__ == '__main__':
	current_action = "default"
	auth_token = None
	while(current_action != "quit"):
		current_action = input("\nPlease specify an action (type help for more information about "
							   "available actions): ")
		match current_action:
			case "register_user":
				register_user()
			case "delete_user":
				auth_token= delete_user(auth_token)
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
			case "list_transactions":
				list_transactions(auth_token)
			case "list_reservations":
				list_reservations(auth_token)
			case "create_reservation":
				create_reservation(auth_token)
			case "update_reservation":
				update_reservation(auth_token)
			case "delete_reservation":
				delete_reservation(auth_token)
			case _:
				if current_action != "quit":
					print("\nInvalid action (type help to list available actions)\n")
