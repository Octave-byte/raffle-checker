import streamlit as st
import requests
import pandas as pd

# Define the campaign mapping
CAMPAIGN_MAPPING = {
    "Monadverse Whitelist Raffle": "1",
    "Wandering Whales Shark Raffle": "2",
    "Pudgy Penguins - Rootstock": "3",
    "Giza": "4",
}

# API configuration
url = "https://api.dune.com/api/v1/query/4786858/results"
headers = {
    "X-DUNE-API-KEY": st.secrets["auth_token"]
}
def check_address_for_raffle(address, raffle):
    address = address.lower()  # Convert address to lowercase
    params = {
        "filters": f"address = '{address}' AND campaign_id = '{raffle}'",
        "columns": "address,cat"
    }
    response = requests.request("GET", url, headers=headers, params=params)
    data = response.json()
    df = pd.DataFrame(data['result']['rows'])
    
    result = {"address": None, "participant": 0, "winner": 0}
    
    if not df.empty:
        address = df["address"].iloc[0]
        result["address"] = address
        result["participant"] = int("participant" in df["cat"].values)
        result["winner"] = int("winner" in df["cat"].values)
    
    return result

# Streamlit UI
st.title("Jumper Raffle Participation and Winner Checker")

# User inputs
address = st.text_input("Enter your wallet address:")
campaign_name = st.selectbox("Select a campaign:", list(CAMPAIGN_MAPPING.keys()))

if st.button("Check Participation"):
    if not address:
        st.error("Please enter your wallet address.")
    else:
        campaign_id = CAMPAIGN_MAPPING[campaign_name]
        result = check_address_for_raffle(address, campaign_id)
        
        if result["address"]:
            st.success(f"Results for {result['address']}")
            st.write(f"**Participating:** {'✅' if result['participant'] else '❌'}")
            st.write(f"**Winning:** {'✅' if result['winner'] else '❌'}")
        else:
            st.warning("No participation found for this address in the selected campaign.")
