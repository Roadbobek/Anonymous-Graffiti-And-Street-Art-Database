import time, socket, sys, sqlite3, os
import json
import threading

# --- Global Storage for Connected Clients ---
# This list will hold all active client sockets
CONNECTED_CLIENT_SOCKETS = []
# This lock will protect access to the CONNECTED_CLIENT_SOCKETS list
CLIENT_SOCKET_LOCK = threading.Lock()

# --- Database Setup ---
db_path = os.path.join("chatroom.db")

# Function to get a new DB connection for each thread/operation
def get_db_connection():
    return sqlite3.connect(db_path, check_same_thread=False)

# Initial DB setup (ensure table exists)
conn_init = get_db_connection()
cursor_init = conn_init.cursor()
cursor_init.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id TEXT,
    name TEXT,
    message TEXT,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn_init.commit()
conn_init.close() # Close initial connection

# --- Client Handler Function (runs in its own thread) ---
def handle_client(client_socket, client_address):
    print(f"Connection Established. Connected From: {client_address}")

    # Add this client's socket to the global list of connected clients
    with CLIENT_SOCKET_LOCK: # Acquire lock before modifying shared list
        CONNECTED_CLIENT_SOCKETS.append(client_socket)
        print(f"Client {client_address} added. Total active clients: {len(CONNECTED_CLIENT_SOCKETS)}")

    try:
        # Server sends its name first
        server_name = "Server"
        client_socket.send(server_name.encode())

        # Server receives client's initial handshake (e.g., their display name)
        client_initial_data = (client_socket.recv(1024)).decode()
        print(f"{client_initial_data} has connected (initial handshake).")

        while True:
            try:
                received_data = client_socket.recv(1024)
                if not received_data: # If connection is closed (empty data)
                    print(f"Client {client_address} disconnected.")
                    break # Exit loop if client disconnected

                decoded_data = received_data.decode()

                try:
                    message_data = json.loads(decoded_data)
                    client_id = message_data.get('id')
                    client_name = message_data.get('name')
                    client_message = message_data.get('message')

                    if client_id and client_name and client_message:
                        full_message_str = f"[{client_name} - {client_id[:4]}...]: {client_message}"
                        print(full_message_str) # Print to server console

                        # Insert into database
                        db_conn = get_db_connection() # Get a new connection for this thread
                        db_cursor = db_conn.cursor()
                        db_cursor.execute("""
                            INSERT INTO messages
                            (id, name, message)
                            VALUES (?, ?, ?)
                        """, (
                            client_id,
                            client_name,
                            client_message
                        ))
                        db_conn.commit()
                        db_conn.close() # Close DB connection after commit
                        print("Message saved to database.")

                        # --- BROADCASTING LOGIC ---
                        # Send the original received JSON message to all *other* connected clients
                        message_to_broadcast = decoded_data.encode() # Re-encode for sending
                        with CLIENT_SOCKET_LOCK: # Acquire lock before iterating shared list
                            for sock in CONNECTED_CLIENT_SOCKETS:
                                if sock != client_socket: # Don't send back to the sender
                                    try:
                                        sock.sendall(message_to_broadcast)
                                    except socket.error as e:
                                        print(f"Error sending to client {sock.getpeername()}: {e}. Removing.")
                                        # Client likely disconnected, remove it (handled in finally for sending client)
                                        # (Robust removal of failed send clients can be more complex)
                    else:
                        print(f"Received incomplete data from client: {decoded_data}")

                except json.JSONDecodeError:
                    print(f"Received non-JSON data or incomplete JSON: {decoded_data}")
                except Exception as e:
                    print(f"Error processing received data from {client_address}: {e}")

            except socket.error as e:
                print(f"Socket error with client {client_address}: {e}")
                break
            except Exception as e:
                print(f"An unexpected error occurred with client {client_address}: {e}")
                break

    finally:
        # Remove this client's socket from the global list when it disconnects or an error occurs
        with CLIENT_SOCKET_LOCK: # Acquire lock before modifying shared list
            if client_socket in CONNECTED_CLIENT_SOCKETS:
                CONNECTED_CLIENT_SOCKETS.remove(client_socket)
                print(f"Client {client_address} removed. Total active clients: {len(CONNECTED_CLIENT_SOCKETS)}")
        print(f"Server handler for {client_address} exiting.")
        client_socket.close() # Ensure client socket is closed

# --- Main Server Listener ---
def start_server():
    server_socket = socket.socket()
    host_name = socket.gethostname()
    s_ip = socket.gethostbyname(host_name)

    port = 4235 # Ensure this matches your client's port

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((host_name, port))
        print("Binding successful!")
        print("Server IP: ", s_ip)
        print(f"Listening on port: {port}")

        server_socket.listen(5) # Listen for up to 5 pending connections
        print("Waiting for connections...")

        while True:
            # This 'accept' now just accepts connections, and hands them off to a new thread
            client_socket, client_address = server_socket.accept()
            print(f"Received connection from {client_address}")
            # Start a new thread to handle this client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.daemon = True # Allows program to exit even if threads are running
            client_thread.start()

    except Exception as e:
        print(f"Error starting server: {e}")
    finally:
        print("Server shutting down.")
        server_socket.close() # Close the main listening socket

if __name__ == "__main__":
    start_server()