import streamlit as st


def get_secret(key):

    return st.secrets[key]