import streamlit as st
import streamlit.components.v1 as components
import base64
import os



# --- Start of Base64 Image Embedding ---
# Get the directory where the current script is located (e.g., 'your_app/pages')
script_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the root of the Streamlit app (e.g., 'your_app')
app_root_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

# Construct the path to the new image: 'your_app/assets/GRAFF_DB-SCALED-NO-BG-(1).png'
image_filename = "GRAFF_DB-SCALED-NO-BG-(1).png"
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
    max-width: 900px; /* SIGNIFICANTLY INCREASED: Set a new maximum width */
    height: auto;   /* Let height adjust proportionally */
    
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 50px auto; /* Centers the container */
    overflow: hidden;
    padding: 20px; 
  }}
  .animated-logo {{
    max-width: 100%; /* Image will scale down to fit its container */
    height: auto;    /* Maintain aspect ratio */
    display: block;  /* Ensures it behaves like a block element */

    /* Animation properties */
    animation: logoGlowFlicker 2s ease-in-out infinite alternate; 
    filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.5));
  }}

  @keyframes logoGlowFlicker {{
    0% {{
      filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.5));
    }}
    50% {{
      filter: drop-shadow(0 0 15px rgba(255, 255, 255, 0.8))
              drop-shadow(0 0 20px rgba(255, 165, 255, 0.6));
    }}
    100% {{
      filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.5));
    }}
  }}
</style>
<div class="logo-container">
  <img src="{image_src_base64}" class="animated-logo" alt="Animated GRAFF DB Logo">
</div>
"""

# Embed the HTML component
# INCREASED HEIGHT: Adjust this to accommodate the larger logo and its glow without clipping.
components.html(animated_logo_html, height=700) # You might need to fine-tune this value



# HTML and CSS for the simple static white glow
animated_logo_html = f"""
<style>
  .logo-container {{
    width: 95%;
    max-width: 900px; /* Adjust max-width as needed */
    height: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 50px auto;
    overflow: hidden;
    padding: 20px; 
  }}
  .animated-logo {{
    max-width: 100%;
    height: auto;
    display: block;
    /* Static filter as requested */
    filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.5)); /* Subtle white glow */
  }}

  /* No @keyframes rule as there's no animation */

</style>
<div class="logo-container">
  <img src="{image_src_base64}" class="animated-logo" alt="Static GRAFF DB Logo">
</div>
"""

# Embed the HTML component
components.html(animated_logo_html, height=700) # Adjust height as needed
