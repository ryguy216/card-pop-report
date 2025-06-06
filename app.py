# app.py

import streamlit as st
import requests
import pandas as pd

# --- Helper Functions ---
def fetch_mock_populations(card_name):
    # Replace with real population fetch logic later
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

def fetch_google_image(card_name):
    # Placeholder: returns a stock image to avoid broken links
    return "https://upload.wikimedia.org/wikipedia/commons/3/36/No_image_available.png"

# --- Streamlit UI ---
st.set_page_config(page_title="Card Population Report", layout="centered")
st.title("📊 Card Population Aggregator")

card_name = st.text_input("🔍 Enter Card Name:")

if card_name:
    st.markdown(f"### Results for **{card_name}**")
    with st.spinner("Fetching data..."):
        image_url = fetch_google_image(card_name)
        population_data = fetch_mock_populations(card_name)
        df = build_dataframe(population_data)

    st.image(image_url, width=250)
    st.dataframe(
        df.style.format("{:.0f}")
        .set_properties(**{"font-weight": "bold"}, subset=pd.IndexSlice[df.index, ["Total"]])
        .set_table_styles([
            {"selector": "th", "props": [("font-size", "14px")]},
            {"selector": "td", "props": [("font-size", "14px")]}])
    )
else:
    st.info("Enter a card name above to view population data.")
