# import streamlit as st
# import random, string
# import threading
# import sqlite3
# import socket
# import json
# import os
#
# # Set how the page looks in browser
# st.set_page_config(
#     page_title="Anonymous Graffiti & Street Art Database",
#     page_icon="🎨",
#     layout="wide"
# )
#
#
# db_path = os.path.join("chatroom.db")
# db = sqlite3.connect(db_path, check_same_thread=False)
# cursor = db.cursor()
#
#
# socket_server = socket.socket()
# server_host = socket.gethostname()
# ip = socket.gethostbyname(server_host)
# sport = 4235 # Ensure this matches server's port
#
# # TODO: Change once website hosted
# server_host = "192.168.172.1"
#
# #Generate a random 10-character alphanumeric ID
# # Note: This does NOT check if the ID is already in the database.
# # For simplicity, we're assuming collision probability is low for a small chat.
# # In a real app, the server would handle ID uniqueness.
# def generate_random_id(length=10):
#     characters = string.ascii_letters + string.digits # A-Z, a-z, 0-9
#     return ''.join(random.choice(characters) for i in range(length))
#
# if 'client_id' not in st.session_state:
#     st.session_state.client_id = generate_random_id()
#
# socket_server.connect((server_host, sport))
#
# # Initial Handshake: Client sends its ID to the server
# # The server expects this, so send your or client_id
# socket_server.send(st.session_state.client_id.encode())
#
# # Receive server's name (response to handshake)
# server_name = socket_server.recv(1024)
# server_name = server_name.decode()
#
#
# # Title of the page
# st.title("🗨️ Chatroom")
# st.divider()
#
# # Use st.session_state for 'user_name' to persist it across reruns,
# # and initialize its value for new sessions.
# if 'user_name' not in st.session_state:
#     st.session_state.user_name = "Anonymous"
#
# # Get input from the text widget
# user_name_input_value = st.text_input(
#     label="What's your name?",
#     value=st.session_state.user_name, # Initialize from current session state
#     key="user_name_input"             # Unique key for the widget
# )
#
# # Process the user's name input
# # 1. Strip leading/trailing whitespace from the input
# cleaned_name = user_name_input_value.strip()
#
# # 2. If the cleaned name is empty (meaning it was empty or only spaces),
# # set the session state name to "Anonymous".
# # Otherwise, use the cleaned name.
# if not cleaned_name:
#     st.session_state.user_name = "Anonymous"
# else:
#     st.session_state.user_name = cleaned_name
#
# # Chat input
# prompt = st.chat_input(f"{st.session_state.user_name}:", max_chars=600)
#
# # Chat message display logic
# if prompt:
#     # Ensure the user_name from session_state is used here
#     if st.session_state.user_name: # Check if it's not empty
#
#         # Create a dictionary to hold ID, name, and message
#         message_data = {
#             'id': st.session_state.client_id,
#             'name': st.session_state.user_name,
#             'message': prompt
#         }
#
#         # Convert the dictionary to a JSON string
#         json_message = json.dumps(message_data)
#
#         # Encode the JSON string to bytes and send it
#         try:
#             socket_server.send(json_message.encode())
#         except socket.error as e:
#             print(f"Error sending message: {e}")
#
#     else:
#         # Fallback if name is somehow empty
#         # Create a dictionary to hold ID, name, and message
#         message_data = {
#             'id': st.session_state.client_id,
#             'name': "Anonymous",
#             'message': prompt
#         }
#
#         # Convert the dictionary to a JSON string
#         json_message = json.dumps(message_data)
#
#         # Encode the JSON string to bytes and send it
#         try:
#             socket_server.send(json_message.encode())
#         except socket.error as e:
#             print(f"Error sending message: {e}")
