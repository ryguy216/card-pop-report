import streamlit as st
import requests
import pandas as pd
from collections import defaultdict

# === CONFIG ===
BING_API_KEY = "YOUR_BING_API_KEY"
BING_SEARCH_URL = "https://api.bing.microsoft.com/v7.0/images/search"

st.set_page_config(page_title="Card Population Report with Images", layout="wide")
st.title("📊 Card Population Report Aggregator with Bing Image Search")
st.write("Enter a card name to search PSA, BGS, SGC, and CGC population counts and get card images from Bing.")

card_name = st.text_input("Card Name")
search_button = st.button("🔍 Search")

def fetch_psa_population(card_name):
    # Mock data due to PSA API limitations
    return {
        "Company": "PSA",
        "Grades": {"10": 12, "9.5": 20, "9": 45, "8": 13},
        "Image": None
    }

def fetch_bgs_population(card_name):
    return {
        "Company": "BGS",
        "Grades": {"10": 15, "9.5": 30, "9": 50, "8.5": 12},
        "Image": None
    }

def fetch_sgc_population(card_name):
    return {
        "Company": "SGC",
        "Grades": {"10": 20, "9.5": 25, "9": 40, "8": 10},
        "Image": None
    }

def fetch_cgc_population(card_name):
    return {
        "Company": "CGC",
        "Grades": {"10": 5, "9.5": 18, "9": 22, "8": 8},
        "Image": None
    }

def merge_population_data(all_results):
    total_by_grade = defaultdict(int)
    all_grades = sorted({grade for result in all_results for grade in result["Grades"]})

    table_data = []
    for grade in all_grades:
        row = {"Grade": grade}
        for result in all_results:
            count = result["Grades"].get(grade, 0)
            if isinstance(count, (int, float)):
                row[result["Company"]] = count
                total_by_grade[grade] += count
            else:
                row[result["Company"]] = 0
        row["Total"] = total_by_grade[grade]
        table_data.append(row)

    return pd.DataFrame(table_data)

def bing_image_search(query):
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    params = {
        "q": query,
        "count": 1,
        "imageType": "Photo",
        "safeSearch": "Moderate",
    }
    try:
        response = requests.get(BING_SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        if "value" in search_results and len(search_results["value"]) > 0:
            return search_results["value"][0]["thumbnailUrl"]
        else:
            return None
    except Exception:
        return None

if search_button and card_name:
    with st.spinner("Fetching population data and images..."):
        results = [
            fetch_psa_population(card_name),
            fetch_bgs_population(card_name),
            fetch_sgc_population(card_name),
            fetch_cgc_population(card_name)
        ]

        # Get Bing image for card
        bing_img_url = bing_image_search(card_name)

        st.subheader("🔎 Bing Image Search Result")
        if bing_img_url:
            st.image(bing_img_url, width=250)
        else:
            st.write("No image found on Bing.")

        st.subheader("📸 Company Population Summaries")
        for result in results:
            st.markdown(f"### {result['Company']}")
            grades = result["Grades"]
            if "Error" in grades:
                st.error(f"Error from {result['Company']}: {grades['Error']}")
                continue
            df = pd.DataFrame(list(grades.items()), columns=["Grade", "Population"])

            # Style grade column bold, hide row numbers
            styled_df = df.style.set_properties(subset=["Grade"], **{"font-weight": "bold"}).hide(axis="index")

            st.dataframe(styled_df)

        st.subheader("📊 Total Population by Grade")
        merged_df = merge_population_data(results)
        # Bold grade column and hide index for total table as well
        styled_total_df = merged_df.style.set_properties(subset=["Grade"], **{"font-weight": "bold"}).hide(axis="index")
        st.dataframe(styled_total_df)
