import streamlit as st
from shillelagh.backends.apsw.db import connect
from streamlit_lottie import st_lottie
from helper import *
import datetime
from uuid import uuid4

st.set_page_config(
    page_title="Language and Identity on Twitter",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state = "expanded",
    menu_items={
         #'Get Help': 'https://www.extremelycoolapp.com/help',
         #'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# Find out your linguistic Twitter profile." }
)

with st.sidebar:
    st.markdown("""👋 **Welcome!** Go to **Home** to enter a Twitter username. 
                Then navigate to **Language** or **Polarization** to find out how your results. 
                """)

lottie_tweet = load_lottieurl('https://assets2.lottiefiles.com/packages/lf20_MUGYrv.json')
st_lottie(lottie_tweet, speed=1, height=200, key="initial")

st.title("Language and Identity on Twitter") 
st.subheader("See multiple linguistic Twitter analysis.")

placeholder = st.empty()
with placeholder.container():
    with st.expander("Consent", expanded=True):
        st.markdown("""
           By submitting the form below you agree to your data being used for research. 
           Your twitter username will be stored in a private google sheet and will not be shared with anyone (unless extraordinary circumstances force us to share it). 
           You can ask for your data to be deleted by emailing us with an ID number you'll be issued after submitting the form. 
           """)
        agree = st.checkbox("I understand and consent.")

if agree:
    placeholder.empty()
    with st.expander("Consent", expanded=False):
        st.markdown("""
           By submitting the form below you agree to your data being used for research. 
           Your twitter username will be stored in a private google sheet and will not be shared with anyone (unless extraordinary circumstances force us to share it). 
           You can ask for your data to be deleted by emailing us with an app ID number you'll be issued after submitting the form. 
           """)
        st.markdown("You have consented.")
    
    st.text_input("Enter a twitter username to begin", key="name", placeholder="e.g. POTUS", value="POTUS")
    st.session_state.username_mine = st.radio(
            "I confirm that",
            ('This username belongs to me.', 'This username is belongs to someone else.')) 
    


st.session_state.submitted = False
st.session_state.disable = True 

if 'username_mine' in st.session_state and st.sesion_state.name != "POTUS" and st.session_state.username_mine == 'This username belongs to me.' and agree:
    form_place = st.empty()
    with form_place.container():
        form = st.expander("Form",expanded=True)
        dem_words, rep_words = [], []
        form.markdown("#### Please add five words that describe Democrats best")
        for i in range(5):
            dem_words.append(form.text_input("D"+str(i+1)))
        st.session_state.dem_words = ", ".join(dem_words).lower()
        form.markdown("#### Please add five words that describe Republicans best")
        for i in range(5):
            rep_words.append(form.text_input("R"+str(i+1),key = "R"+str(i+1)))
        st.session_state.rep_words = ", ".join(rep_words).lower()

        form.markdown("#### Feeling Thermomether")
        form.slider("How warm do you feel about Democrats (0 = coldest rating; 100 = warmest rating)?", 
                    min_value=0, max_value=100, value=50, step=1,key="dem_temp")          
        form.slider("How warm do you feel about Republicans (0 = coldest rating; 100 = warmest rating)?", 
                        min_value=0, max_value=100, value=50, step=1,key="rep_temp") 
        st.session_state.party = form.radio(
                     "How do you identify?",
                    ('Independant','Republican', 'Democrat')) 
        st.session_state.disable = True if st.session_state.R5 == "" else False
 
        form.warning("Please fill out every field of the form to enable the submit button.")              
        st.session_state.submitted = form.button("Submit", disabled=st.session_state.disable)
    if  st.session_state.submitted:
        form_place.empty()

    with st.expander("Thank you",expanded=True):
        if st.session_state.submitted:
            st.session_state.id = datetime.now().strftime('%Y%m-%d%H-%M-') + str(uuid4())
            st.success("Thanks for submitting your answers!")
            st.markdown(f"Your app ID is {st.session_state.id}. Note it down and email us if you want your answers deleted.") 
                        
            st.session_state.conn = connect(":memory:", 
                            adapter_kwargs = {
                            "gsheetsapi": { 
                            "service_account_info":  st.secrets["gcp_service_account"] 
                                    }
                                        }
                        )
            insert_user_data(conn, st.secrets["private_gsheets_url"])

    
                      
    
if 'username_mine' in st.session_state and st.session_state.username_mine == 'This username is belongs to someone else.':
    with st.expander("Thank you", expanded=True):
        st.session_state.conn = connect(":memory:", 
                    adapter_kwargs = {
                        "gsheetsapi": { 
                        "service_account_info":  st.secrets["gcp_service_account"] 
                                    }
                                        }
                    )
        st.markdown("""You entered someone else's Twitter username. 
                Some analyses will not be available. 
                If you change your mind at any point, return to this page to enter your Twitter username.
                """)
        st.success("Open the sidebar and navigate to **Language** or  **Polarization** to see your results.")




