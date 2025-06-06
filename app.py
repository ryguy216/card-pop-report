# app.py

import streamlit as st
import requests
import pandas as pd

# --- Configuration ---
EBAY_APP_ID = "Your-eBay-App-ID"  # Replace with your actual eBay App ID

# --- Helper Functions ---

def search_ebay_image(card_name):
    try:
        headers = {
            "X-EBAY-C-ENDUSERCTX": "contextualLocation=country=US",
            "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
            "Content-Type": "application/json"
        }
        params = {
            "q": card_name,
            "limit": 1
        }
        url = f"https://api.ebay.com/buy/browse/v1/item_summary/search?q={card_name}&limit=1"
        headers["Authorization"] = f"Bearer {EBAY_APP_ID}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            items = response.json().get("itemSummaries", [])
            if items:
                return items[0].get("image", {}).get("imageUrl")
        return None
    except Exception as e:
        return None

def fetch_mock_populations(card_name):
    # Placeholder function for demo purposes. Replace with actual API/web scraping.
    return {
        "PSA": {"Grades": {"10": 500, "9": 800, "8": 300}},
        "BGS": {"Grades": {"10": 200, "9": 400, "8": 150}},
        "SGC": {"Grades": {"10": 100, "9": 250, "8": 100}},
        "CGC": {"Grades": {"10": 120, "9": 260, "8": 90}}
    }

def build_dataframe(pop_data):
    all_grades = set()
    for data in pop_data.values():
        all_grades.update(data["Grades"].keys())

    sorted_grades = sorted(all_grades, key=lambda x: float(x), reverse=True)
    df = pd.DataFrame(index=sorted_grades)

    for company, data in pop_data.items():
        counts = {grade: data["Grades"].get(grade, 0) for grade in sorted_grades}
        df[company] = pd.Series(counts)

    df["Total"] = df.sum(axis=1)
    df.index.name = "Grade"
    return df

# --- Streamlit UI ---
st.set_page_config(page_title="Card Population Report", layout="wide")
st.title("Card Population Aggregator")

card_name = st.text_input("Enter Card Name (e.g., 2018 Panini Hoops Luka Doncic RC):")

if card_name:
    st.subheader(f"Results for: {card_name}")
    with st.spinner("Fetching data..."):
        image_url = search_ebay_image(card_name)
        population_data = fetch_mock_populations(card_name)
        df = build_dataframe(population_data)

    if image_url:
        st.image(image_url, width=250)
    else:
        st.info("No image found.")

    st.dataframe(df.style.format("{:.0f}"))
else:
    st.info("Please enter a card name above to see population and image data.")
