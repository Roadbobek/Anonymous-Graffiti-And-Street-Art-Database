import time, socket, sys, threading
import random, string # For random ID generation
import json           # For packaging data as JSON

socket_server = socket.socket()
server_host = socket.gethostname() # Typically '127.0.0.1' or your local IP
ip = socket.gethostbyname(server_host)
sport = 4245 # Ensure this matches server's port

print('This is your IP address: ',ip)
server_host = input('Enter friend\'s IP address (e.g., 127.0.0.1 if on same computer):')

#Generate a random 10-character alphanumeric ID
# Note: This does NOT check if the ID is already in the database.
# For simplicity, we're assuming collision probability is low for a small chat.
# In a real app, the server would handle ID uniqueness.
def generate_random_id(length=10):
    characters = string.ascii_letters + string.digits # A-Z, a-z, 0-9
    return ''.join(random.choice(characters) for i in range(length))

client_id = generate_random_id()
print(f"Your unique ID (for this session): {client_id}")

# Ask for client's display name
client_name = input('Enter your display name: ')


socket_server.connect((server_host, sport))

# Initial Handshake: Client sends its name to the server
# The server expects this, so send your client_name (or client_id)
socket_server.send(client_name.encode())

# Receive server's name (response to handshake)
server_name = socket_server.recv(1024)
server_name = server_name.decode()

print(f'{server_name} has joined...')


# Function to send messages
def send_msg():
    while True:
        message_text = input("Me : ") # Get user's message

        # Create a dictionary to hold ID, name, and message
        message_data = {
            'id': client_id,
            'name': client_name,
            'message': message_text
        }

        # Convert the dictionary to a JSON string
        json_message = json.dumps(message_data)

        # Encode the JSON string to bytes and send it
        try:
            socket_server.send(json_message.encode())
        except socket.error as e:
            print(f"Error sending message: {e}")
            break # Exit loop if sending fails (e.g., server disconnected)

# Function to receive messages (currently unused for chatroom, but here for future)
# To make this a chatroom, your server would need to broadcast messages.
# For now, this thread would just wait for server responses.
# def recv_msg():
#     while True:
#         try:
#             response = (socket_server.recv(1024)).decode()
#             print(f"Received from server: {response}")
#         except socket.error as e:
#             print(f"Error receiving message: {e}")
#             break # Exit loop if receiving fails

# --- Start the sending thread ---
t1 = threading.Thread(target=send_msg)
t1.start()

# # Start the receiving thread (UNCOMMENT THIS if your server starts sending you replies/broadcasts)
# t2 = threading.Thread(target=recv_msg)
# t2.start()

# Keep the main thread alive (optional, but good if you want to join threads later)
# t1.join()
# # if 't2' in locals() and t2.is_alive(): # Check if t2 was started
# #     t2.join()