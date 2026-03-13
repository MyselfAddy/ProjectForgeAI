import streamlit as st
import base64

def apply_ui():

    with open("background.png", "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()

    st.markdown(f"""
    <style>

    .stApp {{
        background-image:
        linear-gradient(rgba(0,0,0,0.80), rgba(0,0,0,0.80)),
        url("data:image/jpg;base64,{encoded}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    section[data-testid="stSidebar"] {{
        background: rgba(10,10,10,0.95);
        backdrop-filter: blur(10px);
    }}

    .stButton>button {{
         background: linear-gradient(90deg,#00ADB5,#00FFF5);
         color:black;
         border-radius:10px;
         font-weight:bold;
     }}

     .stDownloadButton>button {{
         background: linear-gradient(90deg,#4CAF50,#7CFC00);
         color:black;
         border-radius:10px;
         font-weight:bold;
     }}


    # </style>
    # """, unsafe_allow_html=True)
