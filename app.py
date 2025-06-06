import streamlit as st
import pandas as pd
from collections import defaultdict

# --- Page Config ---
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
        "Grades": {"10": 12, "9": 45, "8": 13},  # Removed 9.5, 8.5
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
