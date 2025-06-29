import streamlit as st

# Set how the page looks in browser
st.set_page_config(
    page_title="Anonymous Graffiti & Street Art Database",
    page_icon="🎨",
    layout="wide"
)

# Logo of the app
st.logo(image="assets//AG&SAD - no bg - scaled 2.png", size="large")

# Title of the app
st.title("🎨 Anonymous Graffiti & Street Art Database 🎨")
st.divider()

st.image(image="assets//GRAFF DB - SCALED - NO BG (1).png", width=760)

st.write("Welcome to the anonymous graffiti and street art database!")
st.write(r"Use the navigation menu to explore or upload posts.")