import streamlit as st
import streamlit.components.v1 as components
import base64
import os


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


# The Discord SVG icon code
discord_svg = """
<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" class="bi bi-discord" viewBox="0 0 16 16">
  <path d="M13.545 2.907a13.2 13.2 0 0 0-3.257-1.011.05.05 0 0 0-.052.025c-.141.25-.297.577-.406.833a12.2 12.2 0 0 0-3.658 0 8 8 0 0 0-.412-.833.05.05 0 0 0-.052-.025c-1.125.194-2.22.534-3.257 1.011a.04.04 0 0 0-.021.018C.356 6.024-.213 9.047.066 12.032q.003.022.021.037a13.3 13.3 0 0 0 3.995 2.02.05.05 0 0 0 .056-.019q.463-.63.818-1.329a.05.05 0 0 0-.01-.059l-.018-.011a9 9 0 0 1-1.248-.595.05.05 0 0 1-.02-.066l.015-.019q.127-.095.248-.195a.05.05 0 0 1 .051-.007c2.619 1.196 5.454 1.196 8.041 0a.05.05 0 0 1 .053.007q.121.1.248.195a.05.05 0 0 1-.004.085 8 8 0 0 1-1.249.594.05.05 0 0 0-.03.03.05.05 0 0 0 .003.041c.24.465.515.909.817 1.329a.05.05 0 0 0 .056.019 13.2 13.2 0 0 0 4.001-2.02.05.05 0 0 0 .021-.037c.334-3.451-.559-6.449-2.366-9.106a.03.03 0 0 0-.02-.019m-8.198 7.307c-.789 0-1.438-.724-1.438-1.612s.637-1.613 1.438-1.613c.807 0 1.45.73 1.438 1.613 0 .888-.637 1.612-1.438 1.612m5.316 0c-.788 0-1.438-.724-1.438-1.612s.637-1.613 1.438-1.613c.807 0 1.451.73 1.438 1.613 0 .888-.631 1.612-1.438 1.612"/>
</svg>
"""
email_svg = """
<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" class="bi bi-envelope-fill" viewBox="0 0 16 16">
  <path d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414zM0 4.697v7.104l5.803-3.558zM6.761 8.83l-6.57 4.027A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.144l-6.57-4.027L8 9.586zm3.436-.586L16 11.801V4.697z"/>
</svg>
"""
github_svg = """
<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" class="bi bi-github" viewBox="0 0 16 16">
  <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8"/>
</svg>
"""
x_svg = """
<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" class="bi bi-twitter-x" viewBox="0 0 16 16">
  <path d="M12.6.75h2.454l-5.36 6.142L16 15.25h-4.937l-3.867-5.07-4.425 5.07H.316l5.733-6.57L0 .75h5.063l3.495 4.633L12.601.75Zm-.86 13.028h1.36L4.323 2.145H2.865z"/>
</svg>
"""
steam_svg = """
<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" class="bi bi-steam" viewBox="0 0 16 16">
  <path d="M.329 10.333A8.01 8.01 0 0 0 7.99 16C12.414 16 16 12.418 16 8s-3.586-8-8.009-8A8.006 8.006 0 0 0 0 7.468l.003.006 4.304 1.769A2.2 2.2 0 0 1 5.62 8.88l1.96-2.844-.001-.04a3.046 3.046 0 0 1 3.042-3.043 3.046 3.046 0 0 1 3.042 3.043 3.047 3.047 0 0 1-3.111 3.044l-2.804 2a2.223 2.223 0 0 1-3.075 2.11 2.22 2.22 0 0 1-1.312-1.568L.33 10.333Z"/>
  <path d="M4.868 12.683a1.715 1.715 0 0 0 1.318-3.165 1.7 1.7 0 0 0-1.263-.02l1.023.424a1.261 1.261 0 1 1-.97 2.33l-.99-.41a1.7 1.7 0 0 0 .882.84Zm3.726-6.687a2.03 2.03 0 0 0 2.027 2.029 2.03 2.03 0 0 0 2.027-2.029 2.03 2.03 0 0 0-2.027-2.027 2.03 2.03 0 0 0-2.027 2.027m2.03-1.527a1.524 1.524 0 1 1-.002 3.048 1.524 1.524 0 0 1 .002-3.048"/>
</svg>
"""
person_circle_svg = """
<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
  <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
  <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
</svg>
"""


st.title("Anonymous Graffiti & Street Art Database")
st.header("A graffiti and street art database focused on anonymity.")
st.divider()

# ----- GRAFF DB BANNER with custom CSS -----
# --- Start of Base64 Image Embedding ---
# Get the directory where the current script is located (e.g., 'your_app/pages')
script_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the root of the Streamlit app (e.g., 'your_app')
app_root_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

# Construct the path to the new image: 'your_app/assets/GRAFF_DB-SCALED-NO-BG-(1).png'
image_filename = "GRAFF_DB-BANNER.png"
image_path = os.path.join(app_root_dir, "assets", image_filename)

# Check if the image file exists
if not os.path.exists(image_path):
    st.error(f"Error: Image file not found at {image_path}")
    st.info(f"Current script directory: {script_dir}")
    st.info(f"Assumed app root directory: {app_root_dir}")
    st.stop() # Stop execution if image not found

# Read the image file and encode it to Base64
with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    # Set the MIME type for PNG
    image_mime_type = "image/png"

image_src_base64 = f"data:{image_mime_type};base64,{encoded_image}"
# --- End of Base64 Image Embedding ---


# HTML and CSS for the responsive glow/flicker animation
animated_logo_html = f"""
<style>
  .logo-container {{
    /* Make the container responsive and BIGGER */
    width: 95%; /* Take up 95% of its parent's width (Streamlit column) */
    max-width: 900px; /* Set a new maximum width */
    height: auto;   /* Let height adjust proportionally */
    
    display: flex;
    justify-content: flex-start; /* Changed to align left */
    align-items: center;
    margin: 1px 0 1px 0; /* Top/Bottom 50px, Left/Right 0px */
    
    overflow: hidden;
    padding: 20px; 
  }}
  .animated-logo {{
    max-width: 100%; /* Image will scale down to fit its container */
    height: auto;    /* Maintain aspect ratio */
    display: block;  /* Ensures it behaves like a block element */

    /* Animation properties: Using the adapted flicker-in-glow animation logic */
    -webkit-animation: image-flicker-in-glow 4s linear both;
    animation: image-flicker-in-glow 4s linear both;
    /* Initial filter for when animation starts/ends */
    filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.5));
  }}

  /* Adapted animation for images to simulate "text-flicker-in-glow" */
  @-webkit-keyframes image-flicker-in-glow {{
    0% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0)); /* No shadow */
    }}
    10% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    10.1% {{
      opacity: 1;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0)); /* No shadow */
    }}
    10.2% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    20% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    20.1% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.25));
    }}
    20.6% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    30% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    30.1% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.45), 0 0 60px rgba(255, 255, 255, 0.25));
    }}
    30.5% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.45), 0 0 60px rgba(255, 255, 255, 0.25));
    }}
    30.6% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    45% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    45.1% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.45), 0 0 60px rgba(255, 255, 255, 0.25));
    }}
    50% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.45), 0 0 60px rgba(255, 255, 255, 0.25));
    }}
    55% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.45), 0 0 60px rgba(255, 255, 255, 0.25));
    }}
    55.1% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    57% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    57.1% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.55), 0 0 60px rgba(255, 255, 255, 0.35));
    }}
    60% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.55), 0 0 60px rgba(255, 255, 255, 0.35));
    }}
    60.1% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    65% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    65.1% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.55), 0 0 60px rgba(255, 255, 255, 0.35), 0 0 100px rgba(255, 255, 255, 0.1));
    }}
    75% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.55), 0 0 60px rgba(255, 255, 255, 0.35), 0 0 100px rgba(255, 255, 255, 0.1));
    }}
    75.1% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    77% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    77.1% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.55), 0 0 60px rgba(255, 255, 255, 0.4), 0 0 110px rgba(255, 255, 255, 0.2), 0 0 100px rgba(255, 255, 255, 0.1));
    }}
    85% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.55), 0 0 60px rgba(255, 255, 255, 0.4), 0 0 110px rgba(255, 255, 255, 0.2), 0 0 100px rgba(255, 255, 255, 0.1));
    }}
    85.1% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    86% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    86.1% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.6), 0 0 60px rgba(255, 255, 255, 0.45), 0 0 110px rgba(255, 255, 255, 0.25), 0 0 100px rgba(255, 255, 255, 0.1));
    }}
    100% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.6), 0 0 60px rgba(255, 255, 255, 0.45), 0 0 110px rgba(255, 255, 255, 0.25), 0 0 100px rgba(255, 255, 255, 0.1));
    }}
  }}
  @keyframes image-flicker-in-glow {{
    0% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    10% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    10.1% {{
      opacity: 1;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    10.2% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    20% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    20.1% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.25));
    }}
    20.6% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    30% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    30.1% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.45), 0 0 60px rgba(255, 255, 255, 0.25));
    }}
    30.5% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.45), 0 0 60px rgba(255, 255, 255, 0.25));
    }}
    30.6% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    45% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    45.1% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.45), 0 0 60px rgba(255, 255, 255, 0.25));
    }}
    50% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.45), 0 0 60px rgba(255, 255, 255, 0.25));
    }}
    55% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.45), 0 0 60px rgba(255, 255, 255, 0.25));
    }}
    55.1% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    57% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    57.1% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.55), 0 0 60px rgba(255, 255, 255, 0.35));
    }}
    60% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.55), 0 0 60px rgba(255, 255, 255, 0.35));
    }}
    60.1% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    65% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    65.1% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.55), 0 0 60px rgba(255, 255, 255, 0.35), 0 0 100px rgba(255, 255, 255, 0.1));
    }}
    75% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.55), 0 0 60px rgba(255, 255, 255, 0.35), 0 0 100px rgba(255, 255, 255, 0.1));
    }}
    75.1% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    77% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    77.1% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.55), 0 0 60px rgba(255, 255, 255, 0.4), 0 0 110px rgba(255, 255, 255, 0.2), 0 0 100px rgba(255, 255, 255, 0.1));
    }}
    85% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.55), 0 0 60px rgba(255, 255, 255, 0.4), 0 0 110px rgba(255, 255, 255, 0.2), 0 0 100px rgba(255, 255, 255, 0.1));
    }}
    85.1% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    86% {{
      opacity: 0;
      filter: drop-shadow(0 0 0px rgba(255, 255, 255, 0));
    }}
    86.1% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.6), 0 0 60px rgba(255, 255, 255, 0.45), 0 0 110px rgba(255, 255, 255, 0.25), 0 0 100px rgba(255, 255, 255, 0.1));
    }}
    100% {{
      opacity: 1;
      filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.6), 0 0 60px rgba(255, 255, 255, 0.45), 0 0 110px rgba(255, 255, 255, 0.25), 0 0 100px rgba(255, 255, 255, 0.1));
    }}
  }}
</style>
<div class="logo-container">
  <img src="{image_src_base64}" class="animated-logo" alt="Animated GRAFF DB Logo">
</div>
"""

# Embed the HTML component
components.html(animated_logo_html, height=310) # You might need to fine-tune this value
# ----- End of GRAFF DB BANNER with custom CSS -----



st.markdown(
    """
    <div style="display: flex; font-size: 1.5rem; margin-bottom: 0px;">
    I've always had a keen interest in both graffiti and computers.  <br>
    When I was first getting into designing graffiti pieces and making street art, I found it difficult to find a centralized database for inspiration or to quickly check if certain names or styles were overused.  <br>
    This personal challenge was the driving force behind creating this platform.  <br> 
    Contribute anonymously to a worldwide street art database – Discover art from across the globe, or easily find pieces nearest to your location to explore local scenes.
    </div>
    """, unsafe_allow_html=True
)

st.markdown(
    """
    <div style="display: flex; font-size: 1.1rem; margin-top: 12px;">
    Website built with Python and Streamlit.
    Data is stored in an SQLite database.
    The interactive map is powered by streamlit-folium, integrating Folium maps (leveraging Leaflet.js and OpenStreetMap data).  <br>
    Thanks to all the contributors behind these amazing open-source tools and datasets! &nbsp;&nbsp;❤
    </div>
    """, unsafe_allow_html=True
)

st.divider()
st.write("## Contact me:")
st.write("##### If you want to contact me please do so through Discord.")

# Combined Discord icon and text on one line
st.markdown(
    f"""
    <div style="display: flex; align-items: center; font-size: 1.25rem; margin-top: 10px;">
        {discord_svg}&nbsp;Discord:&nbsp;
        <a href="https://discord.com/app" target="_blank" style="color: #007bff; text-decoration: none; font-weight: bold;">Roadbobek</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Combined X icon and text on one line
st.markdown(
    f"""
    <div style="display: flex; align-items: center; font-size: 1.25rem; margin-top: 14px;">
        {x_svg}&nbsp;X:&nbsp;
        <a href="https://x.com/Roadbobek" target="_blank" style="color: #007bff; text-decoration: none; font-weight: bold;">Roadbobek</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Combined Email icon and text on one line
st.markdown(
    f"""
    <div style="display: flex; align-items: center; font-size: 1.25rem; margin-top: 14px;">
        {email_svg}&nbsp;Email:&nbsp;
        <a href="mailto:contact.roadbobek@gmail.com" target="_blank" style="color: #007bff; text-decoration: none; font-weight: bold;">contact.roadbobek@gmail.com</a>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()
st.write("## Other projects:")

# Combined Person Circle icon and text on one line
st.markdown(
    f"""
    <div style="display: flex; align-items: center; font-size: 1.25rem; margin-top: 10px;">
        {person_circle_svg}&nbsp;Portfolio:&nbsp;
        <a href="" target="_blank" style="color: #007bff; text-decoration: none; font-weight: bold;">COMING SOON</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Combined Github icon and text on one line
st.markdown(
    f"""
    <div style="display: flex; align-items: center; font-size: 1.25rem; margin-top: 14px;">
        {github_svg}&nbsp;Github:&nbsp;
        <a href="https://github.com/Roadbobek" target="_blank" style="color: #007bff; text-decoration: none; font-weight: bold;">Roadbobek</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Combined Steam icon and text on one line
st.markdown(
    f"""
    <div style="display: flex; align-items: center; font-size: 1.25rem; margin-top: 14px;">
        {steam_svg}&nbsp;Steam:&nbsp;
        <a href="https://steamcommunity.com/id/Roadbobek/" target="_blank" style="color: #007bff; text-decoration: none; font-weight: bold;">Roadbobek</a>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()
st.text("(oﾟvﾟ)ノ            Scroll down ▽")

# Runs 28 times
for i in range(27):
    st.write("")


st.image("assets//GRAFF_DB-BANNER.png")

# Runs 28 times
for i in range(27):
    st.write("")

st.image("assets//AG&SAD - no bg - scaled 2.png")

# Runs 28 times
for i in range(27):
    st.write("")


st.image("assets//GRAFF_DB-SCALED-NO-BG-(1).png")
st.image("assets//GRAFF DB - NO BG.png")


# Runs 28 times
for i in range(27):
    st.write("")



# import time
# with st.empty():
#     for seconds in range(10):
#         st.write(f"⏳ {seconds} seconds have passed")
#         time.sleep(1)
#         st.write(":material/check: 10 seconds over!")
# st.button("Rerun")

# Create two columns. The first number (0.8) is the width of the left empty column,
# and the second number (0.2) is the width of the right column where your text will go.
col1, col2 = st.columns([0.8, 0.2])
with col1:
    # This column is empty, which pushes the content in col2 to the right
    pass
with col2:
    st.write("###### luv u all 💝")
