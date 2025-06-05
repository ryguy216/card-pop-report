import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def search_psa(card_name):
    import requests
    from bs4 import BeautifulSoup

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    url = f"https://www.psacard.com/pop/search?query={card_name}"
    response = requests.get(url, headers=headers, verify=False)
    
    if response.status_code != 200:
        return "Error: PSA page not reachable"

    soup = BeautifulSoup(response.text, 'html.parser')

    # You can customize the scraping logic here depending on how PSA structures their page
    return "PSA page scraped successfully (placeholder)"


def search_sgc(card_name):
    url = f"https://sgccard.com/population-report?search={card_name.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
   response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    sgc_data = []
    if table:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if cols:
                sgc_data.append([col.get_text(strip=True) for col in cols])
    return sgc_data

def search_bgs_placeholder(card_name):
    return [["BGS scraping not implemented (JavaScript required)"]]

def search_cgc_placeholder(card_name):
    return [["CGC scraping not implemented (JavaScript required)"]]

def to_dataframe(data):
    if not data:
        return pd.DataFrame()
    if len(data) == 0:
        return pd.DataFrame()
    # Use a generic header if unknown
    columns = ["Column " + str(i+1) for i in range(len(data[0]))]
    return pd.DataFrame(data, columns=columns)

def generate_excel(psa, sgc, bgs, cgc):
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        to_dataframe(psa).to_excel(writer, sheet_name="PSA", index=False)
        to_dataframe(sgc).to_excel(writer, sheet_name="SGC", index=False)
        to_dataframe(bgs).to_excel(writer, sheet_name="BGS", index=False)
        to_dataframe(cgc).to_excel(writer, sheet_name="CGC", index=False)
    return output.getvalue()

st.title("Card Grading Population Report Aggregator")

card_name = st.text_input("Enter card name (e.g., 'Charizard 4/102 Base Set')")

if st.button("Search"):
    with st.spinner("Fetching data..."):
        psa = search_psa(card_name)
        sgc = search_sgc(card_name)
        bgs = search_bgs_placeholder(card_name)
        cgc = search_cgc_placeholder(card_name)

    st.subheader("PSA Results")
    st.dataframe(to_dataframe(psa))

    st.subheader("SGC Results")
    st.dataframe(to_dataframe(sgc))

    st.subheader("BGS Results")
    st.dataframe(to_dataframe(bgs))

    st.subheader("CGC Results")
    st.dataframe(to_dataframe(cgc))

    excel_data = generate_excel(psa, sgc, bgs, cgc)
    st.download_button("Download Excel Report", data=excel_data, file_name=f"{card_name.replace(' ', '_')}_pop_report.xlsx")
