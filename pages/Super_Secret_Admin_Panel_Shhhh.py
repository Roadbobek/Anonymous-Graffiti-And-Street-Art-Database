import streamlit as st
from PIL import Image
import sqlite3
import bcrypt
import os


# ——— Page Config & Title ———
st.set_page_config(
    page_title="Anonymous Graffiti & Street Art Database",
    page_icon="🎨",
    layout="wide"
)

# - Sidebar navigation -
st.sidebar.title("Navigation")
st.sidebar.page_link('View.py', label='**View** Posts')
st.sidebar.page_link('pages/2_Upload.py', label='**Upload** New Post')
st.sidebar.page_link('pages/4_About_The_Project.py', label='*About The Project*')


# Apply custom CSS for global styling
st.markdown("""
    <style>
        
        /* Styles for the logo when sidebar is EXPANDED (it's inside the 'stSidebarHeader' div) */
        [data-testid="stSidebarHeader"] img.stLogo {
            width: 240px !important; /* **MAKE IT BIGGER WHEN EXPANDED** */
            height: auto !important; /* Maintain aspect ratio */
        }

        /* Styles for the logo when sidebar is COLLAPSED (it's inside the 'stSidebarCollapsedControl' div) */
        [data-testid="stSidebarCollapsedControl"] img.stLogo {
            width: 120px !important; /* **MAKE IT NORMAL/SMALLER WHEN COLLAPSED** */
            height: auto !important; /* Maintain aspect ratio */
        }

        /* Apply a smooth transition effect to the logo's width */
        /* img.stLogo { */
            /* transition: width 0.3s ease-in-out !important; */
        /* } */
        
    </style>
""", unsafe_allow_html=True)


# --- Paths & DB setup ---
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
upload_dir = os.path.join(parent_dir, "graffiti_uploads")
os.makedirs(upload_dir, exist_ok=True)
db_path = os.path.join(parent_dir, "graffiti.db")
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()


# --- Helper functions ---
def resize_to_fit(path, max_size=(900, 900)):
    """Resizes an image to fit within specified maximum dimensions."""
    img = Image.open(path)
    img.thumbnail(max_size, Image.Resampling.LANCZOS) # Scales proportionally
    return img


# Logo of the app
st.logo(image="assets//GRAFF_DB-BANNER.png", size="large")

# Title of the page
st.header("🔒 Admin Panel")
st.divider() # Divider under header


# --- Secure admin login ---
ADMIN_HASHED_PASSWORD = """$2b$12$S6OJZ4fNJ9Cn2q0K7qi8Q.Xci5HRs73EuEvjkWnPVCouWOfCv2iH2"""

# Admin password input field
password_input = st.text_input("🗝️ Enter admin password:", type="password")

if password_input: # Only try to verify if user has typed something
    # Hash the entered password and compare it with the stored hash
    # bcrypt.checkpw automatically handles salting and comparison
    if bcrypt.checkpw(password_input.encode('utf-8'), ADMIN_HASHED_PASSWORD.encode('utf-8')):
        st.success("Login successful!")
    else:
        st.error("Incorrect password.")
        st.stop() # Stop further execution if password is wrong
else:
    # Display a message if password input is empty
    st.info("Please enter your admin password to proceed.")
    st.stop() # Stop further execution until correct password is provided

st.divider() # Divider under admin login



# --- Display selected post ---
# Initialize posts as an empty list by default, in case of invalid search input
# Makes sure posts always stays a list
posts = []

# Search by post ID
post_id_search = st.text_input("Enter post ID:")

st.divider() # Divider under search bar

# Get post with searched ID
cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id_search,))
# cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id_search,)) # SQLlite
posts = cursor.fetchall() # Fetch results for the ID search

# Unpack post data into post variable
for post in posts:
    # Unpack post data
    post_id, file_name, location, artist, time_taken, description, upload_time, likes, dislikes, reports, lat, lon, removed = post

    # Create two columns for post display
    col1, col2 = st.columns([0.7, 0.3])

    # Show post image
    with col1:
        image_path = os.path.join(parent_dir, "graffiti_uploads", file_name) # Construct image path
        img = resize_to_fit(image_path) # Resize image for display
        st.image(img) # Display image

    with col2:
        with st.container(border=True):
            # Display post ID
            st.write(f"<h2 style='margin-bottom: -35px;'>Post ID: {post_id}</h2>", unsafe_allow_html=True)
            st.divider()

            # Display post artist
            st.write(f"<h5 style='margin-bottom: -35px;'>Artist: {artist or 'Unknown Artist'}</h5>", unsafe_allow_html=True)
            st.divider()

            # Display post location
            st.write(f"<h5 style='margin-bottom: -35px;'>📍 {location or 'Unknown Location'} | [{lat}, {lon}]</h5>", unsafe_allow_html=True)
            st.divider()

            # Display post time stamps
            st.caption(f"<h5 style='margin-bottom: -35px;'>📷 Taken: {time_taken or 'Unknown'} (Uploader's Timezone)  |  ⬆️ Uploaded: {upload_time} (UTC)</h5>", unsafe_allow_html=True)
            st.divider()

            # Display post description
            st.write(f"<h6 style='margin-bottom: -35px;'>{description or "No description provided."}</h6>", unsafe_allow_html=True) # Display description
            st.divider()

            # Display if post is visible or removed
            if removed == 0:
                st.write("<h3 style='margin-bottom: -40px;background-color:DodgerBlue;text-align: center;border:2px solid #3d4044;'>Post is visible.</h3>", unsafe_allow_html=True)
            else:
                st.write("<h3 style='margin-bottom: -40px;background-color:Tomato;text-align: center;border:2px solid #3d4044;'>Post is removed.</h3>", unsafe_allow_html=True)

            st.divider() # Divider between text and button

            # Button to change post state, visible or removed
            if st.button(label="Change REMOVED value", use_container_width=True):
                if removed == 0:
                    cursor.execute("UPDATE posts SET removed = 1 WHERE id = ?", (post_id_search,))
                    conn.commit()
                else:
                    cursor.execute("UPDATE posts SET removed = 0 WHERE id = ?", (post_id_search,))
                    conn.commit()
                st.rerun()

    st.divider() # Divider under post
