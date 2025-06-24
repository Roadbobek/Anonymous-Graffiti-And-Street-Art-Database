# import streamlit as st
# import sqlite3
# import os
# from PIL import Image
# from datetime import datetime
# from pandas import wide_to_long
#
# # Connect to the database or make it
# # Get the directory where the script lives
# script_dir = os.path.dirname(os.path.abspath(__file__))
# # Go one directory up
# parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
# # Construct the full path to the DB
# db_path = os.path.join(parent_dir, "graffiti.db")
# # Connect to the database
# conn = sqlite3.connect(db_path, check_same_thread=False)
# cursor = conn.cursor()
#
# # Set how the page looks in browser
# st.set_page_config(
#     page_title="Anonymous Graffiti & Street Art Database",
#     page_icon="🎨",
#     layout="wide"
# )
#
# st.markdown("""
#     <style>
#         /* Remove rounding on every image */
#         img {
#             border-radius: 0 !important;
#         }
#     </style>
# """, unsafe_allow_html=True)
#
# def resize_to_fit(path, max_size=(900, 900)):
#     img = Image.open(path)
#     img.thumbnail(max_size, Image.Resampling.LANCZOS)  # Scales proportionally
#     return img
#
# @st.dialog("Full Resolution Image", width='large',)
# def show_full_image(post_id: int, file_name: str):
#     """
#     This dialog shows the full-resolution image for a given post.
#     """
#     img_path = os.path.join(parent_dir, "graffiti_uploads", file_name)
#     st.image(img_path, use_container_width=True)  # scales to app width
#
# # Title of the page
# st.title("🔍 Explore Graffiti Posts")
# st.divider()
#
# # Search bar
# search_term = st.text_input("Search by location, artist, or description:")
# if search_term:
#     cursor.execute("""
#     SELECT * FROM posts WHERE location LIKE ? OR artist LIKE ? OR description LIKE ?
#     """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
# else:
#     cursor.execute("SELECT * FROM posts ORDER BY upload_time DESC")
# posts = cursor.fetchall()
#
# # Sorting options
# sort_by = st.selectbox("Sort by:", ["Newest", "Most Liked", "Closest to Me"])
# if sort_by == "Most Liked":
#     posts.sort(key=lambda x: x[7], reverse=True)  # Sort by likes
# elif sort_by == "Closest to Me":
#     st.warning("Geolocation sorting is under development.")
#
# # Display posts
# for post in posts:
#     post_id, file_name, location, artist, time_taken, description, upload_time, likes, dislikes, reports, lat, lon = post
#     st.divider()
#     col1, col2 = st.columns([0.7  , 0.3])
#     with col1:
#         image_path = os.path.join(parent_dir, "graffiti_uploads", file_name)
#         img = resize_to_fit(image_path)
#         st.image(img)
#         # st.image(os.path.join(parent_dir, "graffiti_uploads", file_name), width=970)
#         if st.button("View Full Resolution", key=f"view_full_{post_id}"):
#             show_full_image(post_id, file_name)
#     with col2:
#         st.subheader(" Artist: " + (artist or "Unknown Artist"))
#         st.caption(f" 📍 {location or 'Unknown Location'} | [{lat}, {lon}]")
#         st.caption(f"📷 Taken: {time_taken or 'Unknown'}  |  ⬆️ Uploaded: {upload_time}")
#         st.write(description or "No description provided.")
#         st.caption(f"ID: {post_id}")
#
#         # Row with 3 buttons in one line
#         like_col, dislike_col, report_col = st.columns(3)
#
#         with like_col:
#             if st.button(f"👍 Like ({likes})", key=f"like_{post_id}", use_container_width=True):
#                 cursor.execute("UPDATE posts SET likes = likes + 1 WHERE id = ?", (post_id,))
#                 conn.commit()
#                 st.rerun()
#
#         with dislike_col:
#             if st.button(f"👎 Dislike ({dislikes})", key=f"dislike_{post_id}", use_container_width=True):
#                 cursor.execute("UPDATE posts SET dislikes = dislikes + 1 WHERE id = ?", (post_id,))
#                 conn.commit()
#                 st.rerun()
#
#         with report_col:
#             if st.button(f"🚩 Report ({reports})", key=f"report_{post_id}", use_container_width=True):
#                 cursor.execute("UPDATE posts SET reports = reports + 1 WHERE id = ?", (post_id,))
#                 conn.commit()
#                 st.rerun()
#
#         # # Flag button
#         # with st.expander("🚩 Flag this post"):
#         #     reason = st.text_area("Reason for flagging:", key=f"reason_{post_id}")
#         #     if st.button("Submit Flag", key=f"submit_flag_{post_id}"):
#         #         cursor.execute("INSERT INTO flags (post_id, reason) VALUES (?, ?)", (post_id, reason))
#         #         conn.commit()
#         #         st.success("✅ Post flagged for moderation.")
#         #         # Show all flags if any exist
#         #
#         # cursor.execute("SELECT reason, timestamp FROM flags WHERE post_id = ?", (post_id,))
#         # flags = cursor.fetchall()
#         # if flags:
#         #     with st.expander(f"🚨 {len(flags)} Flag(s) for this post"):
#         #         for reason, ts in flags:
#         #             st.write(f"🕓 {ts}: {reason}")
