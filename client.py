import requests
import getpass

def register_user():
    print("=== User Registration ===")
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Confirm password: ")
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
    url = "http://localhost:8000/account/register/"

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

if __name__ == '__main__':
	current_action= "default"
	token= None
	while(current_action != "quit"):
		current_action= input("specify action: ")
		match current_action:
			case "register_user":
    			register_user()
