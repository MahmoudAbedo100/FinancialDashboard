import streamlit as st

from Pages import commodities, Crypto, ETFs  # Import all pages

# Multi page sidebar navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Choose a page to display", ("Commodities", "Crypto", "ETFs"))

if selection == "Commodities":
    commodities.app()
elif selection == "Crypto":
    Crypto.app()
elif selection == "ETFs":
    ETFs.app()
