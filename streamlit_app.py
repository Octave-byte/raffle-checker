import streamlit as st
import requests
import pandas as pd


# API configuration
url = "https://api.dune.com/api/v1/query/4786858/results"
headers = {
    "X-DUNE-API-KEY": st.secrets["auth_token"]
}


@st.cache_data(ttl=604800)  # Cache for one week (7 days * 24 * 60 * 60)
def fetch_prize_data():
    url = "https://api.dune.com/api/v1/query/4786858/results"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        rows = data['result']['rows']
        return pd.DataFrame(rows)
    else:
        st.error("Failed to fetch data from the prize API.")
        return pd.DataFrame()

# UI
st.title("🏆 Jumper Raffles and Airdrop Finder")
st.markdown("Enter your address below to check if you've won any prizes!")

user_address = st.text_input("Your wallet address (0x...)", max_chars=42).strip().lower()

if st.button("Search for airdrops"):
    if not user_address.startswith("0x") or len(user_address) != 42:
        st.warning("Please enter a valid Ethereum address.")
    else:
        df = fetch_prize_data()

        # Normalize address casing for matching
        df['address'] = df['address'].str.lower()

        user_prizes = df[df['address'] == user_address]

        if not user_prizes.empty:
            st.success(f"🎉 You have won {len(user_prizes)} prize(s)!")
            st.dataframe(user_prizes[['campaign_name', 'token_name', 'amount']])
        else:
            st.info("🔎 No prizes found yet. Keep digging for opportunities on Jumper!")
