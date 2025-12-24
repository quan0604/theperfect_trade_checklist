import streamlit as st
from src.data_engine import fetch_all_watchlist, WATCHLIST
from src.logic import calculate_ema, detect_aoi
import pandas as pd

st.title('Forex Trading Checklist Tool')
st.sidebar.header('Watchlist')
symbols = st.sidebar.multiselect('Symbols', WATCHLIST, default=WATCHLIST[:5])
days_back = st.sidebar.slider('Days Back:', 30, 120, 60)

if st.button('Fetch Data'):
    with st.spinner('Fetching data, please wait...'):
        all_data = fetch_all_watchlist(symbols, days_back)
    for symbol, (tf_dict, errors) in all_data.items():
        st.subheader(f'Symbol: {symbol}')
        for tf, df in tf_dict.items():
            st.write(f'{tf} - Last 5 rows:')
            st.dataframe(df.tail(5))
            df = calculate_ema(df)
            st.line_chart(df['EMA_20'])
        if errors:
            st.error(f'Errors: {errors}')


