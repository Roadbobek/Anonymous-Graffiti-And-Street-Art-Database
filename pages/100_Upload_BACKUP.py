# import streamlit as st
# from captcha.image import ImageCaptcha
# import random, string
# import os
# import sqlite3
# import time
# import re
#
# # One-time session-state initializations
# if 'controllo' not in st.session_state:
#     st.session_state['controllo'] = False
#
# if 'last_upload' not in st.session_state:
#     st.session_state['last_upload'] = None
#
# # Make graffiti_uploads folder
# # 1) Locate this script’s folder
# script_dir = os.path.dirname(os.path.abspath(__file__))
# # 2) Go up one level (where your graffiti.db lives)
# parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
# # 3) Create the uploads folder alongside the DB
# upload_dir = os.path.join(parent_dir, "graffiti_uploads")
# os.makedirs(upload_dir, exist_ok=True)
#
# # Connect to the database or make it
# ## Get the directory where the script lives
# # script_dir = os.path.dirname(os.path.abspath(__file__))
# # # Go one directory up
# # parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
# # Construct the full path to the DB
# db_path = os.path.join(parent_dir, "graffiti.db")
# # Connect to the database
# conn = sqlite3.connect(db_path, check_same_thread=False)
# cursor = conn.cursor()
#
# # Ensure the posts table exists
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS posts (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     file_name TEXT NOT NULL,
#     location TEXT,
#     artist TEXT,
#     time_taken TEXT,
#     description TEXT,
#     upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     likes INTEGER DEFAULT 0,
#     dislikes INTEGER DEFAULT 0,
#     reports INTEGER DEFAULT 0
# )
# """)
# conn.commit()
#
# # Captcha parameters
# length_captcha = 4
# width = 200
# height = 150
#
# # for manual date
# # Precompile the regex for performance
# DATE_REGEX = re.compile(
#     r'^(\d{4})-'          # Year: four digits
#     r'(0[1-9]|1[0-2]|00)-'  # Month: 01–09,10–12, or 00
#     r'(0[1-9]|[12]\d|3[01]|00)$'  # Day: 01–09,10–29,30–31, or 00
# )
#
# def is_invalid_date(s: str) -> bool:
#     """
#     Returns True if `s` is invalid, False if it’s valid.
#     Valid form is YYYY-MM-DD, where MM and DD can each be "00" to indicate unknown,
#     BUT if MM == "00" then DD must also be "00".
#     """
#     m = DATE_REGEX.match(s)
#     if not m:
#         # Doesn’t even fit the basic pattern
#         return True
#
#     year_str, month_str, day_str = m.groups()
#
#     # If year is "0000" then month MUST be "00"
#     if year_str == "0000" and month_str != "00":
#         return True
#
#     # If month is "00" then day MUST be "00"
#     if month_str == "00" and day_str != "00":
#         return True
#
#     # If month != "00", check numeric range
#     if month_str != "00":
#         month = int(month_str)
#         if not (1 <= month <= 12):
#             return True
#
#     # If day != "00", check numeric range
#     if day_str != "00":
#         day = int(day_str)
#         if not (1 <= day <= 31):
#             return True
#
#     # All checks passed
#     return False
#
# # Set how the page looks in browser
# st.set_page_config(
#     page_title="Anonymous Graffiti & Street Art Database",
#     page_icon="🎨",
#     # layout="wide"
# )
#
# st.title("⬆️ Upload a New Graffiti Post")
# st.divider()
#
# # Captcha control with form
#
# def captcha_control():
#     if not st.session_state['controllo']:
#         st.header("💿 Please complete the Captcha")
#
#         # Generate or regenerate captcha code
#         if 'Captcha' not in st.session_state:
#             st.session_state['Captcha'] = ''.join(
#                 random.choices(string.ascii_uppercase, k=length_captcha)
#             )
#
#         # Display form
#         with st.form(key="captcha_form", clear_on_submit=True):
#             col1, col2 = st.columns(2)
#             image = ImageCaptcha(width=width, height=height)
#             data = image.generate(st.session_state['Captcha'])
#             col1.image(data)
#             user_input = col2.text_input("Enter captcha text:")
#             submitted = st.form_submit_button("Verify the code")
#
#             if submitted:
#                 if user_input.strip().lower() == st.session_state['Captcha'].lower():
#                     st.session_state['controllo'] = True
#                     st.success("✅ Captcha correct! Proceeding…")
#                     st.rerun()
#                 elif user_input.strip().lower() == "":
#                     st.error("🚨 Captcha Incomplete, please try again.")
#                     st.session_state['Captcha'] = st.session_state['Captcha']
#                 else:
#                     st.error("🚨 Captcha incorrect, please try again.")
#                     # regenerate for next attempt
#                     st.session_state['Captcha'] = ''.join(
#                         random.choices(string.ascii_uppercase, k=length_captcha)
#                     )
#                     st.rerun()
#
# # Main upload page
#
# def your_main():
#     global time_taken
#     max_len = 50
#     st.header("🎉 You’re not a robot, go ahead!")
#
#     uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "webp"])
#     location = st.text_input("Location (Street, City, State, Country):", max_chars=50)
#     artist = st.text_input("Artist name:", max_chars=50)
#     time_known = st.selectbox("Time of picture selection type:", ("Please select", "Calender", "Manual", "Date unknown"))
#     if time_known == "Calender":
#         time_taken = st.date_input("Time of picture:", min_value='1950-01-01', max_value='today')
#     elif time_known == "Manual":
#         st.markdown("Format: *YYYY-MM-DD* — use *00* for unknown, — e.g.&ensp;&ensp;*2025-00-00*,&ensp;&ensp;*2021-07-00*,&ensp;&ensp;*2024-3-16*.")
#         time_taken = st.text_input('Time of picture', max_chars=10)
#     elif time_known == "Date unknown":
#         time_taken = "0000-00-00"
#     description = st.text_area("Description:", max_chars=500)
#
#     if st.button("Upload Post"):
#         if uploaded_file:
#             if location:
#                 pass
#             else:
#                 st.error("❌ Empty location.")
#                 st.stop()
#             if artist:
#                 pass
#             else:
#                 st.error("❌ Empty artist name.")
#                 st.stop()
#             if time_known == "Please select":
#                 st.error("❌ Please select a date type.")
#                 st.stop()
#             if time_known == "Manual":
#                 if is_invalid_date(time_taken):
#                     st.error("❌ Invalid date format or logic.")
#                     st.stop()
#                 else:
#                     pass
#
#             file_size_mb = round(uploaded_file.size / (1024 * 1024), 2)
#             file_name, file_ext = os.path.splitext(uploaded_file.name)
#             counter = 1
#             new_name = file_name[:max_len] + file_ext
#             if len(file_name) > 50:
#                 st.success("📏 File name exceeds 50 character limit so it was shortened.")
#             full_path = os.path.join(upload_dir, new_name)
#             while os.path.exists(full_path):
#                 new_name = f"{file_name}_{counter}{file_ext}"
#                 full_path = os.path.join(upload_dir, new_name)
#                 counter += 1
#             with open(full_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())
#
#             cursor.execute(
#                 """
#                 INSERT INTO posts (file_name, location, artist, time_taken, description)
#                 VALUES (?, ?, ?, ?, ?)
#                 """,
#                 (new_name, location, artist, time_taken, description)
#             )
#             conn.commit()
#
#             st.success(f"✅ Uploaded {new_name} ({file_size_mb} MB)!")
#         else:
#             st.error("❌ Please upload an image file.")
#
# # App flow
# if not st.session_state['controllo']:
#     captcha_control()
# else:
#     your_main()
