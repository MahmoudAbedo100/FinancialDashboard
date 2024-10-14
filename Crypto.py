import streamlit as st
import pandas as pd
import requests  # works with API Data Loading
from datetime import datetime
import time

# Adding a last updated date sidebar:
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.sidebar.write(f"Last updated: {current_time}")

# Auto-refresh every 5 seconds
st.sidebar.button("Refresh Data Now")  # Optional button to refresh manually
time.sleep(5)  # Sleep for 5 seconds


# Fetch data from coingecko, data will be in GBP
@st.cache_data(ttl=5)
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    parameters = {
        'vs_currency': 'gbp',  # data will be in GBP
        'order': 'market_cap_desc',
        'per_page': 500,
        'page': 1,
        'sparkline': False,
        'price_change_percentage': '24h,7d'
    }
    response = requests.get(url, params=parameters)
    data = response.json()
    return data


# Prepare the fetched data
def prepare_data(data):
    cryptos = []
    for item in data:
        symbol = item.get('symbol', ' ').upper()
        name = item.get('name', 'N/A')
        current_price = item.get('current_price', 'N/A')
        price_change_24h = item.get('price_change_percentage_24h_in_currency', 'N/A')
        price_change_7d = item.get('price_change_percentage_7d_in_currency', 'N/A')
        previous_price = current_price / (1 + price_change_24h / 100) if current_price != 'N/A' else 'N/A'

        cryptos.append({
            "Symbol": symbol,
            "Name": name,
            "Current Price (GBP)": current_price,
            "Previous Day Price": previous_price,
            "24H Change (%)": price_change_24h,
            "7D Change (%)": price_change_7d
        })
    return pd.DataFrame(cryptos)


# Main Streamlit app function
def app():
    st.title("Streamlit CryptoCurrency Dashboard")
    with st.spinner("Fetching Data..."):
        data = fetch_crypto_data()
        df = prepare_data(data)
        df.index += 1  # Index starts at 1 for display purposes

    # Display the dataframe with styling
    st.dataframe(
        df.style.apply(
            lambda x: ['background-color: #90ee90' if v >= 10 else '' for v in x],
            subset=["24H Change (%)"]
        )
    )


if __name__ == "__main__":
    app()
