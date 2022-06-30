
import streamlit as st
from helper import *
from shillelagh.backends.apsw.db import connect

st.set_page_config(
    page_title="Linguistic Analysis",
    page_icon=""
    )

st.title("Linguistic Analysis")

if 'df' not in st.session_state:
    executed_query = get_all_data(conn)
    st.session_state.df = make_dataframe(executed_query)

st.markdown('cat')
