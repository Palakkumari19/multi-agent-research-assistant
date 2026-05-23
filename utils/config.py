import os

import streamlit as st

from dotenv import load_dotenv

load_dotenv()


def get_secret(key):

    try:

        return st.secrets[key]

    except:

        return os.getenv(key)