import streamlit as st
import sqlite3
import os
from PIL import Image
from datetime import datetime
import requests
import folium
from streamlit_folium import st_folium, folium_static
import math
import time
import boto3
from io import BytesIO


# Connect to the database or make it
script_dir = os.path.dirname(os.path.abspath(__file__)) # Get the directory where the script lives
db_path = os.path.join(script_dir, "graffiti.db") # Construct the full path to the DB

conn = sqlite3.connect(db_path, check_same_thread=False) # Connect to the database
cursor = conn.cursor()


# Set how the page looks in browser
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


# Logo of the app
st.logo(image="assets//GRAFF_DB-BANNER.png", size="large")

st.write("<h1 style='text-align: center;margin-bottom: -30px;'>🖼️ View Graffiti Posts</h1>", unsafe_allow_html=True)
# st.title("🖼️ View Graffiti Posts")
st.divider()

# Apply custom CSS for global styling
st.markdown("""
    <style>
        /* Toggle rounding on every image */
        /* 1: Round. (Default) */ 
        /* 0: Don't Round. */
        img {
            border-radius: 1 !important;
        }

        /* FIX FOR ST_FOLIUM CONTAINER HEIGHT */
        /* Targets the specific container that is too tall */
        .st-emotion-cache-1tvzk6f {
            height: 400px !important; /* Force its height to match your map */
            min-height: 400px !important; /* Ensure it doesn't try to expand smaller */
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
        }

        /* Ensure the iframe itself is contained */
        .st-emotion-cache-1tvzk6f > iframe {
            height: 100% !important; /* Make the iframe fill its parent */
            width: 100% !important; /* Make the iframe fill its parent */
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
        }

        /* Ensure elements around it don't push it */
        div[data-testid="stVerticalBlock"] > div.st-emotion-cache-1f06x3p.e1fzmvkb3 { /* Common block container */
             margin-bottom: 0px !important;
        }

    </style>
""", unsafe_allow_html=True)


# Initialize session state variables
for key, default in [
    ('selected_location', None), # Stores the currently selected location (lat, lon tuple)
    ('location_text', ""),       # Stores the display name of the selected location
    ('map_data', None),          # Stores data from st_folium map interactions

    # Separate cooldown timers for each action
    ('like_cooldown_end_time', 0),
    ('dislike_cooldown_end_time', 0),
    ('report_cooldown_end_time', 0),

    # Sets to track posts already liked/disliked/reported by the current user session
    ('liked_posts', set()),      # Stores post_ids that have been liked
    ('disliked_posts', set()),   # Stores post_ids that have been disliked
    ('reported_posts', set()),   # Stores post_ids that have been reported

    # Dictionary to manage local, temporary warning messages (keyed by "action_postID")
    ('active_local_warnings', {}),

    ('r2_object_key_for_dialog', None)
]:
    st.session_state.setdefault(key, default)


# ------- Cloudflare R2 stuff --------
# TODO: COMMENT WHEN DEPLOYING!
from dotenv import load_dotenv # Uncomment for local development if using .env file
load_dotenv() # Load environment variables from .env file (for local testing)


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


def search_nominatim(query):
    """Searches for a location using the Nominatim API."""
    url = "https://nominatim.openstreetmap.org/search"
    r = requests.get(
        url,
        params={"q": query, "format": "json", "limit": 5},
        headers={"User-Agent": "graffiti-app"} # User-Agent is required by Nominatim
    )
    r.raise_for_status() # Raise an exception for HTTP errors
    return r.json()


@st.dialog("Full Resolution Image", width='large',)
def show_full_image_dialog():
    """
    Displays the full-resolution image for a given post in a dialog, fetched from R2.
    It retrieves the r2_object_key from session_state.
    """

    # Retrieve the r2_object_key from session_state
    r2_object_key_for_dialog = st.session_state.get('r2_key_for_dialog')

    if r2_object_key_for_dialog:
        img_data_full = get_image_from_r2(r2_object_key_for_dialog)
        if img_data_full:
            st.image(img_data_full, use_container_width=True) # Display full image from bytes
        else:
            st.error("❌ Could not load full resolution image.")
    else:
        st.warning("❌ No image key found in R2 cloud for full resolution display.")



# Search bar for posts
search_term = st.text_input("Search by location, artist, description, time taken, upload time or ID. (To search by ID type 'id:' followed by the ID number in the search bar):")

# Initialize posts as an empty list by default, in case of invalid search input
# Makes sure posts always stays a list
posts = []

if "id:" in search_term.lower(): # Use .lower() for case-insensitive check
    try:
        # Extract the ID number after "id:"
        # Example: if search_term is "id:10", this gets "10"
        # .strip() removes any leading/trailing whitespace
        post_id_str = search_term.lower().split("id:")[1].strip()
        post_id = int(post_id_str) # Convert to integer

        # Execute search query specifically by ID using a placeholder
        cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        posts = cursor.fetchall() # Fetch results for the ID search

        if not posts: # If no post found for the ID
            st.info(f"No post found with ID: {post_id}")

    except (IndexError, ValueError):
        # Handles cases where "id:" is present but no valid number follows,
        # or if the number cannot be converted to an integer.
        st.warning("Please enter a valid post ID after 'id:'. For example: 'id:123'")
        # posts remains empty as initialized, or becomes empty here.

elif search_term:
    # Execute search query if a search term is provided
    cursor.execute("""
    SELECT * FROM posts WHERE location LIKE ? OR artist LIKE ? OR description LIKE ? OR time_taken LIKE ? OR upload_time LIKE ?
    """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
    posts = cursor.fetchall() # Fetch results for general search

else:
    # Fetch all posts if no search term, ordered by upload time
    cursor.execute("SELECT * FROM posts ORDER BY upload_time DESC")
    posts = cursor.fetchall() # Fetch all posts by upload time




# Sorting options for posts
sort_by = st.selectbox("Sort by:", ["Newest", "Most Liked", "Most Disliked", "Distance", "Most Reports",])

if sort_by == "Most Liked":
    posts.sort(key=lambda x: x[7], reverse=True) # Sort by likes (column 7)

elif sort_by == "Most Disliked":
    posts.sort(key=lambda x: x[8], reverse=True) # Sort by dislikes (column 8)

elif sort_by == "Most Reports":
    posts.sort(key=lambda x: x[9], reverse=True) # Sort by reports (column 9)

elif sort_by == "Distance":

    loc_in = st.text_input("Search location:", st.session_state['location_text'], max_chars=500)

    if loc_in and len(loc_in) > 2:
        matches = search_nominatim(loc_in) # Search for location matches
        opts = [m['display_name'] for m in matches] # Extract display names for select box
        sel = st.selectbox("Suggestions:", opts, key="loc_sug") # Display suggestions

        if sel:
            idx = opts.index(sel) # Get index of selected suggestion
            lat = float(matches[idx]['lat']) # Convert latitude to float
            lon = float(matches[idx]['lon']) # Convert longitude to float

            st.session_state['selected_location'] = (lat, lon) # Store selected coordinates
            st.session_state['location_text'] = matches[idx]['display_name'] # Store location display name


    st.divider() # Adds a horizontal divider


    # Map picker section
    st.subheader("4. Map Picker (Optional)")

    # Set initial map zoom and coordinates
    initial_zoom = 2
    coords = st.session_state['selected_location'] or (20, 0) # Use selected location or default to (20, 0)
    m = folium.Map(location=coords, zoom_start=initial_zoom) # Create the Folium map


    # Add a marker if a location is selected
    if st.session_state['selected_location']:
        folium.Marker(location=coords, tooltip="Selected Location").add_to(m)

    st.session_state['map_data'] = st_folium(m, width=700, height=400) # Render the interactive map


    # Create a placeholder for the location info message
    location_info_placeholder = st.empty()

    # Display the location info in the placeholder using st.write
    if st.session_state['selected_location'] is not None:
        location_info_placeholder.write(f"###### **📍 [{st.session_state['selected_location'][0]}, {st.session_state['selected_location'][1]}]**")


    # Handle map click events
    if st.session_state['map_data'].get("last_clicked"):
        lat = st.session_state['map_data']["last_clicked"]["lat"] # Get latitude from map click
        lon = st.session_state['map_data']["last_clicked"]["lng"] # Get longitude from map click

        st.session_state['selected_location'] = (lat, lon) # Update selected location with click data

        # Reverse geocode to get location name for display
        resp = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat":lat, "lon":lon, "format":"json"},
            headers={"User-Agent":"graffiti-app"}
        ).json()
        name = resp.get("display_name", "Unknown location")
        st.session_state['location_text'] = name

        st.rerun() # Trigger rerun to update the placeholder with the new selected_location


    # Sort by distance
    # Define the key function for sorting by Great-Circle Distance (Haversine-like)
    # This function accesses 'selected_ref_lat' and 'selected_ref_lon' from the outer scope
    def sort_by_location_key(post_item):
        # Earth's radius in kilometers (as specified in your analysis)
        R = 6371

        # Check if the post's lat/lon values are valid (not None)
        # Assuming longitude is at index 10 and latitude at index 11 in the post_item tuple
        if post_item[10] is None or post_item[11] is None:
            # Assign a very large distance (infinity) to push posts with unknown locations to the end
            return float('inf')

        try:
            # Extract post's longitude and latitude, convert to float
            post_lat = float(post_item[10])
            post_lon = float(post_item[11])

            # Convert all degrees to radians for calculations
            # Reference point (selected by user)
            ref_lon_rad = math.radians(selected_ref_lon)
            ref_lat_rad = math.radians(selected_ref_lat)

            # Post point
            post_lon_rad = math.radians(post_lon)
            post_lat_rad = math.radians(post_lat)

            # Calculate 3D Cartesian coordinates for both points on a unit sphere
            # Point A (Reference)
            x_A = math.cos(ref_lon_rad) * math.cos(ref_lat_rad)
            y_A = math.sin(ref_lon_rad) * math.cos(ref_lat_rad)
            z_A = math.sin(ref_lat_rad)

            # Point B (Post)
            x_B = math.cos(post_lon_rad) * math.cos(post_lat_rad)
            y_B = math.sin(post_lon_rad) * math.cos(post_lat_rad)
            z_B = math.sin(post_lat_rad)

            # Calculate the dot product (A • B)
            # This is equal to cos(theta), where theta is the central angle
            cos_theta = (x_A * x_B) + (y_A * y_B) + (z_A * z_B)

            # Clamp cos_theta to [-1, 1] to avoid floating point errors with math.acos
            # that might result in values slightly outside this range
            cos_theta = max(-1.0, min(1.0, cos_theta))

            # Calculate the central angle (theta) in radians
            theta = math.acos(cos_theta)

            # Calculate the Great-Circle Distance
            distance = R * theta
            return distance

        except ValueError as e:
            # This handles cases where float() conversion or math.acos() might fail
            # (e.g., non-numeric data in lat/lon or ACOS input out of range)
            return float('inf') # Treat as invalid, push to end


    if st.session_state['selected_location'] is not None:
        # Unpack the selected latitude and longitude from session state
        # These variables are now accessible within the sort_by_location_key function's scope
        selected_ref_lat, selected_ref_lon = st.session_state['selected_location']

        # Sort posts by the calculated great-circle distance (smaller distance first)
        posts.sort(key=sort_by_location_key, reverse=False)

    else:
        # If no location is selected, inform the user
        st.warning("Please select a location above to sort by 'Distance'.")
        # If no location is selected, posts will retain their previous sort order.

st.divider()



# Display posts section
for post in posts:

    # Unpack post data
    post_id, r2_object_key, location, artist, time_taken, description, upload_time, likes, dislikes, reports, lat, lon, removed = post

    # Create two columns for post display
    col1, col2 = st.columns([0.7, 0.3])

    if removed == 0:
        with col1:
            img_data = get_image_from_r2(r2_object_key) # Use r2_object_key to get image data
            img = resize_to_fit(img_data) # Resize image for display
            st.image(img) # Display image

            # Pass the r2_object_key to the dialog for full resolution
            if st.button("View Full Resolution", key=f"view_full_{post_id}"):
                st.session_state['r2_key_for_dialog'] = r2_object_key # A dedicated key for the dialog, store the posts r2_object_key
                show_full_image_dialog() # Call the decorated dialog function to open it


        with col2:
            st.subheader("Artist: " + (artist or "Unknown Artist")) # Display artist or "Unknown"

            # Display location details
            st.caption(f"📍 {location or 'Unknown Location'} | [{lat}, {lon}]")
            st.caption(f"📷 Taken: {time_taken or 'Unknown'} (Uploader's Timezone)  |  ⬆️ Uploaded: {upload_time} (UTC)")
            st.write(description or "No description provided.") # Display description
            st.caption(f"ID: {post_id}") # Display post ID



            # ----- Like/Dislike/Report Logic -----
            # Row with like, dislike, and report buttons
            like_col, dislike_col, report_col = st.columns(3)


            # --- LIKE BUTTON LOGIC ---
            with like_col:
                # Determine button text based on whether it's already liked
                is_liked_by_user = post_id in st.session_state['liked_posts']
                like_button_text = f"❌ Unlike ({likes})" if is_liked_by_user else f"👍 Like ({likes})"

                if st.button(like_button_text, key=f"like_{post_id}", use_container_width=True):
                    current_time = time.time()
                    message_content = ""
                    cooldown_duration = 5 # seconds for like cooldown

                    if is_liked_by_user:
                        # If already liked, remove the like
                        cursor.execute("UPDATE posts SET likes = likes - 1 WHERE id = ?", (post_id,))
                        conn.commit()
                        st.session_state['liked_posts'].remove(post_id) # Remove from liked set
                    elif current_time < st.session_state['like_cooldown_end_time']:
                        # If not liked, but cooldown is active
                        time_left = st.session_state['like_cooldown_end_time'] - current_time
                        message_content = f"⌚ Like cooldown: Please wait {time_left:.2f}s."
                    else:
                        # If not liked and cooldown is clear, perform like action
                        cursor.execute("UPDATE posts SET likes = likes + 1 WHERE id = ?", (post_id,))
                        conn.commit()
                        st.session_state['liked_posts'].add(post_id) # Add to liked set
                        st.session_state['like_cooldown_end_time'] = current_time + cooldown_duration # Set new like cooldown

                    # Store message for display via local placeholder and trigger rerun
                    # Only store if message_content is not empty
                    if message_content: # <-- NEW: Only store if there's actual content
                        st.session_state['active_local_warnings'][f"like_warn_{post_id}"] = {
                            "content": message_content,
                            "display_until": current_time + 1.5 # All messages display for 1.5 seconds
                        }
                    st.rerun() # Crucial: Force a rerun to update the UI

                # Create a placeholder for THIS specific post's like-related warnings/messages
                # Moved: local_like_message_placeholder is now created AFTER the button
                local_like_message_placeholder = st.empty()

                # --- Logic to Display/Clear the LOCAL Like Warning on Each Rerun ---
                # This block runs for EVERY post on EVERY rerun to manage its specific warning.
                warning_key = f"like_warn_{post_id}"
                current_time_display = time.time()

                if warning_key in st.session_state.get('active_local_warnings', {}):
                    warning_info = st.session_state['active_local_warnings'][warning_key]

                    if current_time_display < warning_info['display_until']:
                        local_like_message_placeholder.warning(warning_info['content'])

                        # --- JavaScript for Automatic Disappearance (still necessary for true auto-timer) ---
                        # This JavaScript tells the browser to reload the page after 'delay_ms'
                        delay_ms = max(0, int((warning_info['display_until'] - current_time_display) * 1000) + 50)
                        st.markdown(
                            f"""
                            <script>
                                setTimeout(function() {{
                                    window.location.reload();
                                }}, {delay_ms});
                            </script>
                            """,
                            unsafe_allow_html=True
                        )
                        # --- End JavaScript ---
                    else:
                        # Display time has passed: remove the warning from session state and clear placeholder
                        del st.session_state['active_local_warnings'][warning_key]
                        local_like_message_placeholder.empty() # Explicitly clear
                else:
                    local_like_message_placeholder.empty() # Ensure empty if no warning active for this post



            # --- DISLIKE BUTTON LOGIC ---
            with dislike_col:
                # Determine button text based on whether it's already disliked
                is_disliked_by_user = post_id in st.session_state['disliked_posts']
                dislike_button_text = f"❌ Undislike ({dislikes})" if is_disliked_by_user else f"👎 Dislike ({dislikes})"

                if st.button(dislike_button_text, key=f"dislike_{post_id}", use_container_width=True):
                    current_time = time.time()
                    message_content = ""
                    cooldown_duration = 5 # seconds for dislike cooldown

                    if is_disliked_by_user:
                        # If already disliked, remove the dislike
                        cursor.execute("UPDATE posts SET dislikes = dislikes - 1 WHERE id = ?", (post_id,))
                        conn.commit()
                        st.session_state['disliked_posts'].remove(post_id) # Remove from disliked set
                    elif current_time < st.session_state['dislike_cooldown_end_time']:
                        # If not disliked, but cooldown is active
                        time_left = st.session_state['dislike_cooldown_end_time'] - current_time
                        message_content = f"⌚ Dislike cooldown: Please wait {time_left:.2f}s."
                    else:
                        # If not disliked and cooldown is clear, perform dislike action
                        cursor.execute("UPDATE posts SET dislikes = dislikes + 1 WHERE id = ?", (post_id,))
                        conn.commit()
                        st.session_state['disliked_posts'].add(post_id) # Add to disliked set
                        st.session_state['dislike_cooldown_end_time'] = current_time + cooldown_duration # Set new dislike cooldown

                    if message_content: # <-- NEW: Only store if there's actual content
                        st.session_state['active_local_warnings'][f"dislike_warn_{post_id}"] = {
                            "content": message_content,
                            "display_until": current_time + 1.5
                        }
                    st.rerun()

                # Moved: local_dislike_message_placeholder is now created AFTER the button
                local_dislike_message_placeholder = st.empty()

                # --- Logic to Display/Clear the LOCAL Dislike Warning ---
                warning_key = f"dislike_warn_{post_id}"
                current_time_display = time.time()

                if warning_key in st.session_state.get('active_local_warnings', {}):
                    warning_info = st.session_state['active_local_warnings'][warning_key]
                    if current_time_display < warning_info['display_until']:
                        local_dislike_message_placeholder.warning(warning_info['content'])
                        delay_ms = max(0, int((warning_info['display_until'] - current_time_display) * 1000) + 50)
                        st.markdown(f"""<script>setTimeout(function() {{window.location.reload();}}, {delay_ms});</script>""", unsafe_allow_html=True)
                    else:
                        del st.session_state['active_local_warnings'][warning_key]
                        local_dislike_message_placeholder.empty()
                else:
                    local_dislike_message_placeholder.empty()



            # --- REPORT BUTTON LOGIC ---
            with report_col:
                # For report, if already reported, button text can change or it can be disabled
                is_reported_by_user = post_id in st.session_state['reported_posts']
                report_button_text = f"✅ Reported ({reports})" if is_reported_by_user else f"🚩 Report ({reports})"

                if st.button(report_button_text, key=f"report_{post_id}", use_container_width=True):
                    current_time = time.time()
                    message_content = ""
                    cooldown_duration = 5 # seconds for report cooldown

                    if is_reported_by_user:
                        # If already reported, just show a warning (no unreport action for simplicity)
                        # message_content = "✋ You've already reported this post!"
                        pass
                    elif current_time < st.session_state['report_cooldown_end_time']:
                        # If not reported, but cooldown is active
                        time_left = st.session_state['report_cooldown_end_time'] - current_time
                        message_content = f"⌚ Report cooldown: Please wait {time_left:.2f}s."
                    else:
                        # If not reported and cooldown is clear, perform report action
                        cursor.execute("UPDATE posts SET reports = reports + 1 WHERE id = ?", (post_id,))
                        conn.commit()
                        st.session_state['reported_posts'].add(post_id) # Add to reported set
                        st.session_state['report_cooldown_end_time'] = current_time + cooldown_duration # Set new report cooldown
                        message_content = "🚩 Post reported!"

                    if message_content: # <-- NEW: Only store if there's actual content
                        st.session_state['active_local_warnings'][f"report_warn_{post_id}"] = {
                            "content": message_content,
                            "display_until": current_time + 1.5
                        }
                    st.rerun()

                # Moved: local_report_message_placeholder is now created AFTER the button
                local_report_message_placeholder = st.empty()

                # --- Logic to Display/Clear the LOCAL Report Warning ---
                warning_key = f"report_warn_{post_id}"
                current_time_display = time.time()

                if warning_key in st.session_state.get('active_local_warnings', {}):
                    warning_info = st.session_state['active_local_warnings'][warning_key]
                    if current_time_display < warning_info['display_until']:
                        local_report_message_placeholder.warning(warning_info['content'])
                        delay_ms = max(0, int((warning_info['display_until'] - current_time_display) * 1000) + 50)
                        st.markdown(f"""<script>setTimeout(function() {{window.location.reload();}}, {delay_ms});</script>""", unsafe_allow_html=True)
                    else:
                        del st.session_state['active_local_warnings'][warning_key]
                        local_report_message_placeholder.empty()
                else:
                    local_report_message_placeholder.empty()


        st.divider() # Add a divider between posts
