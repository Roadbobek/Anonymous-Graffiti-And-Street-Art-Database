import streamlit as st
import sqlite3
import os
from PIL import Image
from datetime import datetime
import requests
import folium
from streamlit_folium import st_folium, folium_static
import math


# Connect to the database or make it
script_dir = os.path.dirname(os.path.abspath(__file__)) # Get the directory where the script lives
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir)) # Go one directory up
db_path = os.path.join(parent_dir, "graffiti.db") # Construct the full path to the DB

conn = sqlite3.connect(db_path, check_same_thread=False) # Connect to the database
cursor = conn.cursor()


# Set how the page looks in browser
st.set_page_config(
    page_title="Anonymous Graffiti & Street Art Database",
    page_icon="🎨",
    layout="wide"
)


# Apply custom CSS for global styling
st.markdown("""
    <style>
        /* Remove rounding on every image */
        img {
            border-radius: 0 !important;
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


st.markdown("""
    <style>
        /* Remove rounding on every image */
        img {
            border-radius: 0 !important;
        }
    </style>
""", unsafe_allow_html=True)


# Initialize session state variables
for key, default in [
    ('selected_location', None), # Stores the currently selected location (lat, lon tuple)
    ('location_text', ""),       # Stores the display name of the selected location
    ('map_data', None)           # Stores data from st_folium map interactions
]:
    st.session_state.setdefault(key, default)


def resize_to_fit(path, max_size=(900, 900)):
    """Resizes an image to fit within specified maximum dimensions."""
    img = Image.open(path)
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
def show_full_image(post_id: int, file_name: str):
    """
    Displays the full-resolution image for a given post in a dialog.
    """
    img_path = os.path.join(parent_dir, "graffiti_uploads", file_name)
    st.image(img_path, use_container_width=True) # Scales to app width




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




# Display posts section
for post in posts:
    # Unpack post data
    post_id, file_name, location, artist, time_taken, description, upload_time, likes, dislikes, reports, lat, lon = post

    st.divider() # Add a divider between posts

    # Create two columns for post display
    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        image_path = os.path.join(parent_dir, "graffiti_uploads", file_name) # Construct image path
        img = resize_to_fit(image_path) # Resize image for display
        st.image(img) # Display image

        if st.button("View Full Resolution", key=f"view_full_{post_id}"):
            show_full_image(post_id, file_name) # Open full resolution dialog

    with col2:
        st.subheader(" Artist: " + (artist or "Unknown Artist")) # Display artist or "Unknown"

        # Display location details
        st.caption(f" 📍 {location or 'Unknown Location'} | [{lat}, {lon}]")
        st.caption(f"📷 Taken: {time_taken or 'Unknown'}  |  ⬆️ Uploaded: {upload_time}")
        st.write(description or "No description provided.") # Display description
        st.caption(f"ID: {post_id}") # Display post ID


        # Row with like, dislike, and report buttons
        like_col, dislike_col, report_col = st.columns(3)

        with like_col:
            if st.button(f"👍 Like ({likes})", key=f"like_{post_id}", use_container_width=True):
                cursor.execute("UPDATE posts SET likes = likes + 1 WHERE id = ?", (post_id,)) # Increment likes
                conn.commit() # Commit changes to DB
                st.rerun() # Rerun to update counts

        with dislike_col:
            if st.button(f"👎 Dislike ({dislikes})", key=f"dislike_{post_id}", use_container_width=True):
                cursor.execute("UPDATE posts SET dislikes = dislikes + 1 WHERE id = ?", (post_id,)) # Increment dislikes
                conn.commit() # Commit changes to DB
                st.rerun() # Rerun to update counts

        with report_col:
            if st.button(f"🚩 Report ({reports})", key=f"report_{post_id}", use_container_width=True):
                cursor.execute("UPDATE posts SET reports = reports + 1 WHERE id = ?", (post_id,)) # Increment reports
                conn.commit() # Commit changes to DB
                st.rerun() # Rerun to update counts
