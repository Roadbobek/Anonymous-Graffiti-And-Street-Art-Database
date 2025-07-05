import streamlit as st
from captcha.image import ImageCaptcha
import random, string
import os
import sqlite3
import re
import folium
from streamlit_folium import st_folium, folium_static
import requests
import time


# ——— Page Config & Title ———
st.set_page_config(
    page_title="Anonymous Graffiti & Street Art Database",
    page_icon="🎨",
    layout="centered"
)

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

st.title("⬆️ Upload a New Graffiti Post")
st.divider()


# ——— Session‑state init ———
for key, default in [
    ('controllo', False),
    ('selected_location', None),
    ('location_text', ""),
    ('post_cooldown_end_time', 0)
]:
    st.session_state.setdefault(key, default)

# ——— Paths & DB setup ———
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
upload_dir = os.path.join(parent_dir, "graffiti_uploads")
os.makedirs(upload_dir, exist_ok=True)
db_path = os.path.join(parent_dir, "graffiti.db")
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT NOT NULL,
    location TEXT,
    artist TEXT,
    time_taken TEXT,
    description TEXT,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    likes INTEGER DEFAULT 0,
    dislikes INTEGER DEFAULT 0,
    reports INTEGER DEFAULT 0,
    latitude REAL,
    longitude REAL,
    removed INTEGER DEFAULT 0
)
""")
conn.commit()

# ——— Helpers ———
DATE_REGEX = re.compile(
    r'^(\d{4})-(0[1-9]|1[0-2]|00)-(0[1-9]|[12]\d|3[01]|00)$'
)
def is_invalid_date(s: str) -> bool:
    m = DATE_REGEX.match(s)
    if not m:
        return True
    y, mo, d = m.groups()
    if y=="0000" and mo!="00": return True
    if mo=="00" and d!="00": return True
    if mo!="00" and not (1<=int(mo)<=12): return True
    if d!="00" and not (1<=int(d)<=31): return True
    return False

def search_nominatim(query):
    url = "https://nominatim.openstreetmap.org/search"
    r = requests.get(
        url,
        params={"q": query, "format": "json", "limit": 5},
        headers={"User-Agent": "graffiti-app"}
    )
    r.raise_for_status()
    return r.json()

# ——— Captcha control ———
def captcha_control():
    if not st.session_state['controllo']:
        st.header("💿 Please complete the Captcha")
        st.session_state.setdefault(
            'Captcha',
            ''.join(random.choices(string.ascii_uppercase, k=4))
        )
        with st.form("captcha_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            img = ImageCaptcha(width=200, height=150)
            c1.image(img.generate(st.session_state['Captcha']))
            inp = c2.text_input("Enter Captcha:")
            ok = st.form_submit_button("Verify")
            if ok:
                if inp.strip().lower() == st.session_state['Captcha'].lower():
                    st.session_state['controllo'] = True
                    st.success("✅ Captcha correct!")
                    st.rerun()
                else:
                    st.error("🚨 Wrong Captcha, try again.")
                    st.session_state['Captcha'] = ''.join(
                        random.choices(string.ascii_uppercase, k=4)
                    )
                    st.rerun()


# ——— Main upload page ———
def your_main():
    st.subheader("🎉 You’re not a robot — upload away!")
    st.divider()

    # 1) Image upload
    st.subheader("1. Upload Image")
    uploaded_file = st.file_uploader(
        "Choose an image file:", type=["jpg","jpeg","png","webp"]
    )
    st.divider()

    # 2) Artist name
    st.subheader("2. Artist Name")
    artist = st.text_input("Artist name:", max_chars=50)
    st.divider()

    # 3) Location choice
    st.subheader("3. Location")
    loc_method = st.selectbox(
        "Location entry method:",
        ["Please select", "Search & map", "Unknown location"]
    )
    loc_ready = False

    if loc_method == "Search & map":
        loc_in = st.text_input(
            "Search location:",
            st.session_state['location_text'],
            max_chars=500
        )
        if loc_in and len(loc_in) > 2:
            matches = search_nominatim(loc_in)
            opts = [m['display_name'] for m in matches]
            sel = st.selectbox("Suggestions:", opts, key="loc_sug")
            if sel:
                idx = opts.index(sel)
                lat = float(matches[idx]['lat'])
                lon = float(matches[idx]['lon'])
                st.session_state['selected_location'] = (lat, lon)
                st.session_state['location_text'] = matches[idx]['display_name']
                loc_ready = True

    elif loc_method == "Unknown location":
        st.markdown("_Location will be recorded as Unknown_")
        st.session_state['location_text'] = "Unknown"
        st.session_state['selected_location'] = None
        loc_ready = True

    # else:
    #     st.warning("❗ Please choose a location entry method above")
    st.divider()

    # 4) Map picker
    st.subheader("4. Map Picker (Optional)")
    # show full world at zoom 2
    initial_zoom = 2
    coords = st.session_state['selected_location'] or (20, 0)
    m = folium.Map(location=coords, zoom_start=initial_zoom)

    if loc_method == "Search & map":
        # interactive map immediately
        if st.session_state['selected_location']:
            folium.Marker(location=coords, tooltip="Selected Location").add_to(m)
        map_data = st_folium(m, width=700, height=400)

        if map_data.get("last_clicked"):
            lat = map_data["last_clicked"]["lat"]
            lon = map_data["last_clicked"]["lng"]
            st.session_state['selected_location'] = (lat, lon)
            resp = requests.get(
                "https://nominatim.openstreetmap.org/reverse",
                params={"lat":lat, "lon":lon, "format":"json"},
                headers={"User-Agent":"graffiti-app"}
            ).json()
            name = resp.get("display_name", "Unknown location")
            st.session_state['location_text'] = name
            loc_ready = True
            # st.success(f"📍 {name}")

    else:
        # static embed for other methods
        folium_static(m, width=700, height=400)

    st.divider()

    # 5) Time input
    st.subheader("5. Time of Picture")
    time_sel = st.selectbox(
        "Time type:", ["Please select", "Calender", "Manual", "Unknown"]
    )
    if time_sel == "Calender":
        time_taken = st.date_input(
            "Picture date:", min_value="1950-01-01", max_value="today"
        )
    elif time_sel == "Manual":
        st.markdown("Format: YYYY-MM-DD (00 for unknown)")
        time_taken = st.text_input("Enter date:", max_chars=10)
    else:
        time_taken = "0000-00-00"
    st.divider()

    # 6) Description
    st.subheader("6. Description")
    description = st.text_area("Description:", max_chars=500)
    st.divider()

    # 7) Upload button & final validation
    if st.button("Upload Post", use_container_width=True, type="primary"):
        if time.time() < st.session_state['post_cooldown_end_time']:
            st.warning(f"⌚ Please wait {abs(time.time() - st.session_state['post_cooldown_end_time']):.2f} seconds before uploading a new post.")
        else:

            if not uploaded_file:
                st.error("❌ Please upload an image."); st.stop()
            if not artist:
                st.error("❌ Artist name required."); st.stop()
            if loc_method == "Please select":
                st.error("❌ Please choose a location entry method."); st.stop()
            if loc_method == "Search & map" and not loc_ready:
                st.error("❌ You must pick a suggested or click on the map."); st.stop()
            if time_sel == "Please select":
                st.error("❌ Select a time type."); st.stop()
            if time_sel == "Manual" and is_invalid_date(time_taken):
                st.error("❌ Invalid date format."); st.stop()

            # Save image file
            base, ext = os.path.splitext(uploaded_file.name)
            base = base[:50]
            new_name = base + ext
            path = os.path.join(upload_dir, new_name)
            i = 1
            while os.path.exists(path):
                new_name = f"{base}_{i}{ext}"
                path = os.path.join(upload_dir, new_name)
                i += 1
            with open(path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Insert into DB
            lonlat = st.session_state['selected_location'] or (None, None)
            cursor.execute("""
                INSERT INTO posts
                (file_name, location, artist, time_taken, description, latitude, longitude)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                new_name,
                st.session_state['location_text'],
                artist,
                str(time_taken),
                description,
                lonlat[0],
                lonlat[1]
            ))
            conn.commit()
            st.success(f"✅ Uploaded {new_name} successfully!")


        # Start 5 second cooldown
        cooldown_duration_seconds = 5
        if time.time() >= st.session_state['post_cooldown_end_time']:
            st.session_state['post_cooldown_end_time'] = time.time() + cooldown_duration_seconds


# ——— App flow ———
if not st.session_state['controllo']:
    captcha_control()
else:
    your_main()
