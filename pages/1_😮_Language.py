
import streamlit as st
from helper import *
from shillelagh.backends.apsw.db import connect

st.set_page_config(
    page_title="Linguistic Analysis",
    page_icon=""
    )

st.title("Linguistic Analysis")

if 'conn' not in st.session_state:
    st.warning("Please go to the homepage and add a twitter username")
elif 'df' not in st.session_state:
    pass