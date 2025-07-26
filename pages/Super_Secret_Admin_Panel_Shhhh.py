import streamlit as st
from PIL import Image
# import sqlite3
import bcrypt
import os
import psycopg2
import boto3
from io import BytesIO


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


# -------------- PostgresSQL Stuff --------------
# --- Retrieve PostgreSQL credentials from environment variables ---
# These variables are loaded into the app's environment by systemd
DB_HOST = os.getenv("PG_DB_HOST")
DB_NAME = os.getenv("PG_DB_NAME")
DB_USER = os.getenv("PG_DB_USER")
DB_PASSWORD = os.getenv("PG_DB_PASSWORD")
DB_PORT = os.getenv("PG_DB_PORT", "5432") # Default PostgreSQL port, provide a fallback


# --- Database Connection Function (using Streamlit's cache_resource for efficiency) ---
@st.cache_resource
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        st.error(f"Failed to connect to the database: {e}")
        st.stop() # Crucial for deployed apps: stop if DB connection fails
        return None # In case st.stop() doesn't immediately exit

# --- Establish the connection for your app ---
conn = get_db_connection() # This will be your connection object
if conn:
    cursor = conn.cursor() # This will be your cursor object


# --- Paths & DB setup ---
# script_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
# upload_dir = os.path.join(parent_dir, "graffiti_uploads")
# os.makedirs(upload_dir, exist_ok=True)
# db_path = os.path.join(parent_dir, "graffiti.db")
# conn = sqlite3.connect(db_path, check_same_thread=False)
# cursor = conn.cursor()


# ------- Cloudflare R2 stuff --------
# TO-DO: COMMENT WHEN DEPLOYING!
# from dotenv import load_dotenv # Uncomment for local development if using .env file
# load_dotenv() # Load environment variables from .env file (for local testing)


# --- R2 Configuration (assuming environment variables are set) ---
R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")


# Check if essential R2 variables are available
if not all([R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME]):
    st.error("Error: R2 credentials or bucket name are not set as environment variables.")
    st.stop() # Stop the app if configuration is missing

# Construct the R2 endpoint URL
R2_ENDPOINT_URL = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
R2_REGION = "auto" # R2 is globally distributed

# Initialize the S3 client for R2
try:
    s3_client = boto3.client(
        service_name="s3",
        endpoint_url=R2_ENDPOINT_URL,
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name=R2_REGION
    )
    # Optional: A quick test to confirm connectivity (e.g., list buckets). This can be removed in production.
    # s3_client.list_buckets()
    # st.sidebar.success("✅ Connected to Cloudflare R2!") # For debugging
except Exception as e:
    st.error(f"Failed to connect to Cloudflare R2: {e}. Please check your credentials.")
    st.stop()


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


# ------Helper functions------
# Assuming s3_client and R2_BUCKET_NAME are defined and initialized
def get_image_from_r2(object_key: str):
    """
    Retrieves an image from Cloudflare R2 given its object key.
    Returns bytes of the image data, or None if an error occurs.
    """
    try:
        response = s3_client.get_object(Bucket=R2_BUCKET_NAME, Key=object_key)
        image_data = response['Body'].read()
        return image_data
    except Exception as e:
        st.error(f"Error retrieving image '{object_key}' from R2: {e}")
        return None


def resize_to_fit(image_data, max_size=(900, 900)): # Takes image_data (bytes)
    """Resizes an image (from bytes) to fit within specified maximum dimensions."""
    if isinstance(image_data, bytes): # Check if input is bytes
        img = Image.open(BytesIO(image_data)) # Open from bytes using BytesIO
    else:
        # This 'else' block would be for local file paths if you still needed them,
        # but for R2, we'll primarily use the 'bytes' path.
        # If you want to keep old local file compatibility, you could add:
        # img = Image.open(image_data) # Assuming image_data is a path here
        raise ValueError("image_data must be bytes or a file-like object.") # Better error for unexpected input

    img.thumbnail(max_size, Image.Resampling.LANCZOS) # Scales proportionally
    return img



# # --- Helper functions ---
# def resize_to_fit(path, max_size=(900, 900)):
#     """Resizes an image to fit within specified maximum dimensions."""
#     img = Image.open(path)
#     img.thumbnail(max_size, Image.Resampling.LANCZOS) # Scales proportionally
#     return img


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



# Post search and "No post found" message
posts = []
post_id_to_query = None

# Handle post ID search
if post_id_search:
    try:
        post_id_to_query = int(post_id_search) # Convert input to int
        # Execute DB query for the given ID
        cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id_to_query,))
        posts = cursor.fetchall()

    except ValueError:
        st.error("Invalid Post ID format. Please enter a number.")
        posts = [] # Clear posts on invalid input
        post_id_to_query = None # Reset to prevent "No post found" for non-numeric input
else:
    pass # No action if search input is empty

# Display "No post found" message if search performed but no results
if post_id_search and not posts and post_id_to_query is not None:
    st.warning(f"No post found with ID: {post_id_to_query}")


# # Get post with searched ID
# if post_id_search:
#     cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id_search,))
#     posts = cursor.fetchall() # Fetch results for the ID search
# else:
#     pass
#     # st.warning("Enter post ID to search.")
#
# # cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id_search,)) # SQLlite
# # posts = cursor.fetchall() # Fetch results for the ID search



# Unpack post data into post variable
for post in posts:
    # Unpack post data
    post_id, r2_object_key, location, artist, time_taken, description, upload_time, likes, dislikes, reports, lat, lon, removed = post
    # post_id, file_name, location, artist, time_taken, description, upload_time, likes, dislikes, reports, lat, lon, removed = post

    # Create two columns for post display
    col1, col2 = st.columns([0.7, 0.3])

    # Show post image
    with col1:
        img_data = get_image_from_r2(r2_object_key) # Use r2_object_key to get image data
        img = resize_to_fit(img_data) # Resize image for display
        st.image(img) # Display image
        # image_path = os.path.join(parent_dir, "graffiti_uploads", file_name) # Construct image path
        # img = resize_to_fit(image_path) # Resize image for display
        # st.image(img) # Display image

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
                    cursor.execute("UPDATE posts SET removed = 1 WHERE id = %s", (post_id_search,))
                    #cursor.execute("UPDATE posts SET removed = 1 WHERE id = ?", (post_id_search,))
                    conn.commit()
                else:
                    cursor.execute("UPDATE posts SET removed = 0 WHERE id = %s", (post_id_search,))
                    #cursor.execute("UPDATE posts SET removed = 0 WHERE id = ?", (post_id_search,))
                    conn.commit()
                st.rerun()

    st.divider() # Divider under post
