
import streamlit as st
from helper import *
from shillelagh.backends.apsw.db import connect

st.set_page_config(
    page_title="Language",
    page_icon="😮",
    layout="wide"
    )

with st.sidebar:
    st.markdown("""👋 **Welcome!** Go to **Home** to enter a Twitter username. 
                Then navigate to **Language** or **Polarization** to find out how your results. 
                """)

st.title("😮 Language 😮")

if 'conn' not in st.session_state:
    st.warning("Please go to the homepage and add a twitter username")
elif 'df' not in st.session_state:
    pass