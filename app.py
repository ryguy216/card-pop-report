import streamlit as st
import requests
import pandas as pd
from collections import defaultdict

# === CONFIG ===
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
GOOGLE_CSE_ID = "YOUR_GOOGLE_CSE_ID"

st.set_page_config(page_title="Card Population Report with Images", layout="wide")
st.title("📊 Card Population Report Aggregator with Google Image Search")
st.write("Enter a card name to search PSA, BGS, SGC, and CGC population counts and get card images from Google.")

card_name = st.text_input("Card Name")
search_button = st.button("🔍 Search")

def fetch_psa_population(card_name):
    url = "https://www.psacard.com/api/population/card/search"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    payload = {
        "filters": {"term": card_name},
        "page": 1,
        "size": 10
    }

    try:
        response = requests.post(url, json=payload, headers=headers, verify=False)
        data = response.json()

        results = defaultdict(int)
        for card in data.get("results", []):
            for item in card.get("grades", []):
                grade = item.get("label")
                pop = item.get("population", 0)
                results[grade] += pop

        return {"Company": "PSA", "Grades": dict(results), "Image": None}

    except Exception as e:
        return {"Company": "PSA", "Grades": {"Error": str(e)}, "Image": None}

# Mock functions for other graders
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

def google_image_search(query):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": query,
        "searchType": "image",
        "num": 1,
        "imgSize": "medium",
        "safe": "off"
    }
    try:
        resp = requests.get(search_url, params=params)
        data = resp.json()
        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]["link"]
        else:
            return None
    except Exception as e:
        return None

if search_button and card_name:
    with st.spinner("Fetching population data and images..."):
        results = [
            fetch_psa_population(card_name),
            fetch_bgs_population(card_name),
            fetch_sgc_population(card_name),
            fetch_cgc_population(card_name)
        ]

        # Get a Google image for the card overall
        google_img_url = google_image_search(card_name)

        st.subheader("🔎 Google Image Search Result")
        if google_img_url:
            st.image(google_img_url, width=250)
        else:
            st.write("No image found on Google.")

        st.subheader("📸 Company Population Summaries")
        for result in results:
            st.markdown(f"### {result['Company']}")
            grades = result["Grades"]
            if "Error" in grades:
                st.error(f"Error from {result['Company']}: {grades['Error']}")
                continue
            df = pd.DataFrame(list(grades.items()), columns=["Grade", "Population"])
            st.dataframe(df)

        st.subheader("📊 Total Population by Grade")
        merged_df = merge_population_data(results)
        st.dataframe(merged_df)
