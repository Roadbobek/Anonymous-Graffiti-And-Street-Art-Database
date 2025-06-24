# LEGACY ADMIN PANEL CODE
# TODO REVAMP!

# import streamlit as st
# import sqlite3
#
# # Secure admin login
# ADMIN_PASSWORD = "admin123"  # Replace with a hashed password in production
#
# password = st.text_input("Enter admin password:", type="password")
# if password != ADMIN_PASSWORD:
#     st.error("Incorrect password.")
#     st.stop()
#
# # Connect to the database
# conn = sqlite3.connect("../graffiti.db", check_same_thread=False)
# cursor = conn.cursor()
#
# # Title of the page
# st.header("🔒 Admin Panel")
# st.divider()
# # Show flagged posts
# cursor.execute("SELECT * FROM posts WHERE flagged = TRUE")
# flagged_posts = cursor.fetchall()
#
# if not flagged_posts:
#     st.info("No flagged posts.")
# else:
#     for post in flagged_posts:
#         post_id, file_name, location, artist, description, _, _, _ = post
#         st.subheader(artist or "Unknown Artist")
#         st.image(f"../graffiti_uploads/{file_name}", width=200)
#         st.write(description or "No description provided.")
#         st.caption(f"📍 {location or 'Unknown Location'}")
#
#         # Resolve flag
#         if st.button("Resolve Flag", key=f"resolve_{post_id}"):
#             cursor.execute("UPDATE posts SET flagged = FALSE WHERE id = ?", (post_id,))
#             cursor.execute("DELETE FROM flags WHERE post_id = ?", (post_id,))
#             conn.commit()
#             st.success("Flag resolved.")