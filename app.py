import streamlit as st
import pandas as pd
from collections import defaultdict

# --- Page Setup ---
st.set_page_config(page_title="Card Pop Report", layout="wide")
st.markdown("<h1 style='text-align: center;'>📈 Multi-Grader Card Population Report</h1>", unsafe_allow_html=True)

# --- Input ---
with st.container():
    st.markdown("Enter a card name to fetch population counts from **PSA**, **BGS**, **SGC**, and **CGC**.")
    card_name = st.text_input("Card Name", placeholder="e.g. 2018 Panini Prizm Luka Doncic #280")
    search_button = st.button("🔍 Search Pop Reports")

# --- Placeholder Image URL ---
PLACEHOLDER_IMAGE = "https://via.placeholder.com/250x350?text=No+Image"

# --- Fetch Population Functions ---
def fetch_psa_population(card_name):
    return {
        "Company": "PSA",
        "Grades": {
            "10": 12,
            "9": 45,
            "8": 13
        },
        "Image": None
    }

def fetch_bgs_population(card_name):
    return {
        "Company": "BGS",
        "Grades": {
            "10": 15,
            "9.5": 30,
            "9": 50,
            "8.5": 12
        },
        "Image": None
    }

def fetch_sgc_population(card_name):
    return {
        "Company": "SGC",
        "Grades": {
            "10": 20,
            "9.5": 25,
            "9": 40,
            "8": 10
        },
        "Image": None
    }

def fetch_cgc_population(card_name):
    return {
        "Company": "CGC",
        "Grades": {
            "10": 5,
            "9.5": 18,
            "9": 22,
            "8": 8
        },
        "Image": None
    }

# --- Merge and Style ---
def merge_population_data(all_results):
    total_by_grade = defaultdict(int)
    all_grades = sorted({grade for result in all_results for grade in result["Grades"]})

    table_data = []
    for grade in all_grades:
        row = {"Grade": grade}
        for result in all_results:
            company = result["Company"]
            count = result["Grades"].get(grade, 0)
            row[company] = count
            total_by_grade[grade] += count
        row["Total Population"] = total_by_grade[grade]
        table_data.append(row)

    return pd.DataFrame(table_data)

def style_df_bold_grades(df):
    return df.style.set_properties(subset=["Grade"], **{"font-weight": "bold"}).hide(axis="index")

# --- Main Logic ---
if search_button and card_name.strip():
    with st.spinner("Gathering data..."):
        results = [
            fetch_psa_population(card_name),
            fetch_bgs_population(card_name),
            fetch_sgc_population(card_name),
            fetch_cgc_population(card_name)
        ]

        # --- Image Display ---
        st.markdown("### 🖼️ Card Image Preview")
        st.image(PLACEHOLDER_IMAGE, width=250, caption="Image placeholder", use_column_width=False)

        # --- Individual Tables ---
        st.markdown("### 📋 Grader Population Tables")
        col1, col2 = st.columns(2)
        for i, result in enumerate(results):
            with col1 if i % 2 == 0 else col2:
                st.markdown(f"#### {result['Company']}")
                df = pd.DataFrame(list(result["Grades"].items()), columns=["Grade", "Population"])
                st.table(style_df_bold_grades(df))

        # --- Merged Table ---
        st.markdown("### 📊 Combined Total Population by Grade")
        merged_df = merge_population_data(results)
        st.table(style_df_bold_grades(merged_df))
