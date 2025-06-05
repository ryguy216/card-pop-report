import streamlit as st
import requests
import pandas as pd
from collections import defaultdict

st.set_page_config(page_title="Card Population Report", layout="wide")
st.title("📊 Card Population Report Aggregator")
st.write("Enter a card name to search PSA, BGS, SGC, and CGC population counts by grade.")

card_name = st.text_input("Card Name")
search_button = st.button("🔍 Search")

# PSA population fetch via API with SSL verification disabled
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

        return {"Company": "PSA", "Grades": dict(results), "Image": "https://via.placeholder.com/150?text=PSA"}

    except Exception as e:
        return {"Company": "PSA", "Grades": {"Error": str(e)}, "Image": None}

# Sample placeholders for other companies
def fetch_bgs_population(card_name):
    return {
        "Company": "BGS",
        "Grades": {"10": 15, "9.5": 30, "9": 50, "8.5": 12},
        "Image": "https://via.placeholder.com/150?text=BGS"
    }

def fetch_sgc_population(card_name):
    return {
        "Company": "SGC",
        "Grades": {"10": 20, "9.5": 25, "9": 40, "8": 10},
        "Image": "https://via.placeholder.com/150?text=SGC"
    }

def fetch_cgc_population(card_name):
    return {
        "Company": "CGC",
        "Grades": {"10": 5, "9.5": 18, "9": 22, "8": 8},
        "Image": "https://via.placeholder.com/150?text=CGC"
    }

# Merge population data by grade (with type check)
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

# Search trigger
if search_button and card_name:
    with st.spinner("Fetching population data..."):
        results = [
            fetch_psa_population(card_name),
            fetch_bgs_population(card_name),
            fetch_sgc_population(card_name),
            fetch_cgc_population(card_name)
        ]

        st.subheader("📸 Company Summaries")
        for result in results:
            col1, col2 = st.columns([1, 4])
            with col1:
                image_url = result.get("Image")
                if image_url and image_url.startswith("http"):
                    st.image(image_url, width=120)
                else:
                    st.write("No image")
            with col2:
                st.markdown(f"**{result['Company']}**")
                for grade, count in result["Grades"].items():
                    st.write(f"{grade}: {count}")

        st.subheader("📊 Total Population by Grade")
        merged_df = merge_population_data(results)
        st.dataframe(merged_df)
