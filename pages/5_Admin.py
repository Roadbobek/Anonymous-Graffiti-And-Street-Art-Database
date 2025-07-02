import streamlit as st
import sqlite3
import os

# ——— Paths & DB setup ———
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
upload_dir = os.path.join(parent_dir, "graffiti_uploads")
os.makedirs(upload_dir, exist_ok=True)
db_path = os.path.join(parent_dir, "graffiti.db")
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()


# Title of the page
st.header("🔒 Admin Panel")
st.divider()


# Secure admin login
ADMIN_PASSWORD = "admin123"  # Replace with a hashed password in production

password = st.text_input("Enter admin password:", type="password")
if password != ADMIN_PASSWORD:
    st.error("Incorrect password.")
    st.stop()


# Initialize posts as an empty list by default, in case of invalid search input
# Makes sure posts always stays a list
posts = []

post_id_search = st.text_input("Enter post ID:")

cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id_search,))
posts = cursor.fetchall() # Fetch results for the ID search

for post in posts:
    # Unpack post data
    post_id, file_name, location, artist, time_taken, description, upload_time, likes, dislikes, reports, lat, lon, removed = post

    st.divider()
    st.subheader(f"Post ID: {post_id}")
    if removed == 0:
        st.subheader("Post is visible.")
    else:
        st.subheader("Post is removed.")

    if st.button(label="Change REMOVED value"):
        if removed == 0:
            cursor.execute("UPDATE posts SET removed = 1 WHERE id = ?", (post_id_search,))
            conn.commit()
        else:
            cursor.execute("UPDATE posts SET removed = 0 WHERE id = ?", (post_id_search,))
            conn.commit()
        st.rerun()
