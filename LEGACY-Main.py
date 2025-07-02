import streamlit as st


# Set how the page looks in browser
st.set_page_config(
    page_title="Anonymous Graffiti & Street Art Database",
    page_icon="🎨",
    layout="wide"
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
        img.stLogo {
            transition: width 0.3s ease-in-out !important;
        }
        
    </style>
""", unsafe_allow_html=True)


# Logo of the app
st.logo(image="assets//GRAFF_DB-BANNER.png", icon_image="assets//GRAFF_DB-BANNER.png", size="large")

# Title of the app
st.title("🎨 Anonymous Graffiti & Street Art Database 🎨")
st.divider()



st.image(image="assets//GRAFF_DB-SCALED-NO-BG-(1).png", width=760)

st.write("Welcome to the anonymous graffiti and street art database!")
st.write(r"Use the navigation menu to explore or upload posts.")
