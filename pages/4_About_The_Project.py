import streamlit as st

# Set how the page looks in browser
st.set_page_config(
    page_title="Anonymous Graffiti & Street Art Database",
    page_icon="🎨",
    layout="wide"
)

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


st.title("🎨 Anonymous Graffiti & Street Art Database 🎨")
st.divider()

st.markdown(
    """
    <div style="display: flex; font-size: 1.5rem; margin-bottom: 0px;">
    I've always had an interest in both graffiti and computers.  <br>
    When I was getting into graffiti, I found it difficult to find a database for inspiration or to check if certain names were overused.  <br>
    That's why I created this platform.
    </div>
    """, unsafe_allow_html=True
)

st.markdown(
    """
    <div style="display: flex; font-size: 1.1rem; margin-top: 12px;">
    Built with Python and Streamlit.
    The interactive map is powered by streamlit-folium, integrating Folium maps (leveraging Leaflet.js and OpenStreetMap data).  <br>
    Thanks to all the contributors behind these amazing open-source tools! &nbsp;&nbsp;❤
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
# Combined Email icon and text on one line
st.markdown(
    f"""
    <div style="display: flex; align-items: center; font-size: 1.25rem; margin-top: 14px;">
        {email_svg}&nbsp;Email:&nbsp;
        <a href="mailto:Roadbobek1234@gmail.com" target="_blank" style="color: #007bff; text-decoration: none; font-weight: bold;">Roadbobek1234@gmail.com</a>
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

# Runs 8 times
for i in range(7):
    st.write("")

st.image("assets//AG&SAD - no bg - scaled 2.png")
st.image("assets//GRAFF DB - NO BG.png")
# st.image("assets//GRAFF DB - NO BG - GREEN.png")
st.image("assets//GRAFF DB - SCALED - NO BG (1).png")
# st.image("assets//GRAFF DB.png")

# Runs 12 times
for i in range(11):
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
