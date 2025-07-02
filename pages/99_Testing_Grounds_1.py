import streamlit as st
from streamlit.components.v1 import html


# --- Define your javascript ---
my_js = """
alert("Hola mundo");
"""
# Wrap the javascript as html code
my_html = f"<script>{my_js}</script>"



st.title("Javascript example")

html(my_html)


