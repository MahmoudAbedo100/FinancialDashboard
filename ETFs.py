import streamlit as st
import pandas as pd
import yfinance as yf


def fetch_data(symbol):
    etf = yf.Ticker(symbol)
    info = etf.info
    return {
        "Name": info.get('longName', 'N/A'),  # Getting ETF info and attributes
        "Latest Price": info.get('previousClose', 'N/A'),
        "52W High": info.get('fiftyTwoWeekHigh', 'N/A'),
        "52W Low": info.get('fiftyTwoWeekLow', 'N/A'),
        "Total Assets": info.get('totalAssets', 'N/A'),
    }


def app():
    st.title("ETF Analysis")
    file_path = 'ETFs.txt'
    try:
        with open(file_path, 'r') as file:
            symbols = [line.strip().upper() for line in file.readlines()]
            data = [fetch_data(symbol) for symbol in symbols]  # fetching data for every symbol (ETF)
            df = pd.DataFrame(data)  # building data frame of data list
            st.table(df)  # converting it to table
    except FileNotFoundError:
        st.error("ETF File is not accessible")


if __name__ == "__main__":
    app()
