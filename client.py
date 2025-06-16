import requests
from getpass import getpass
import json

server_url= "http://localhost:8000/"

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
		"update_reservation (authenticated users only): allows you to change the number of tickes of a reservation \n\n",
		"delete_reservation (authenticated users only): allows you to delete a reservation \n"
	)
	
def delete_user(auth_token):
	if auth_token != None:
		url= server_url + "account/delete/"
		choice= input("are you sure you want to delete your account? (y/n): ")
		if choice=="y":
			response= requests.delete(url)
			if response.status_code == 204:
				print("deletion succesful\n")
			else:
				print("deletion failed\n")
		else:
			print("deletion cancelled\n")
	else:
		print("you are not logged in")
		
def login(auth_token):
	url= server_url + "account/token/"
	username= input("enter your username: ")
	password= getpass("enter your password: ")
	data= {
		"username": username,
		"password": password
	}
	response= requests.post(url, json=data)	
	
	if response.status_code == 200:
		auth_token= response.json()["token"]
		print("login successful\n")
	else:
		print("login failed\n")

def logout(auth_token):
	auth_token= None
	print("logged out\n")
	
def list_events():
	url= server_url + "events/list/"
	response= requests.get(url)
	
	print("\navailable events:\n")
	print(response.json())

if __name__ == '__main__':
	current_action = "default"
	auth_token = None
	while(current_action != "quit"):
		current_action = input("please specify an action (type help for more information about available actions): ")
		match current_action:
			case "register_user":
				register_user()
			case "help":
				help()
			case "login":
				login(auth_token)
			case "list_events":
				list_events()
			case _:
				if(current_action != "quit"):
					print("invalid command (type help to list available actions)")  			
    			
    			
    			
    			
    			
    			
    			
    			
    			
    			
    			
    			
    			
    			
    			
    			
    			
    			
    			
    			
    			
    			
    			
