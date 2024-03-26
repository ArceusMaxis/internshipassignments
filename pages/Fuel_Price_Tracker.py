import streamlit as st
import requests
from bs4 import BeautifulSoup

def fetch_tn_petrol_price():
    url = "https://www.businesstoday.in/fuel-price/petrol-price-in-chennai-today"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_element = soup.find(id="render_today_price")
    if price_element:
        return price_element.text.strip()
    else:
        return 
    
def fetch_tn_diesel_price():
    url = "https://www.businesstoday.in/fuel-price/diesel-price-in-chennai-today"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_element = soup.find(id="render_today_price")
    if price_element:
        return price_element.text.strip()
    else:
        return None

def fetch_py_petrol_price():
    url = "https://www.businesstoday.in/fuel-price/petrol-price-in-pondicherry-today"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_element = soup.find(id="render_today_price")
    if price_element:
        return price_element.text.strip()
    else:
        return 
    
def fetch_py_diesel_price():
    url = "https://www.businesstoday.in/fuel-price/diesel-price-in-pondicherry-today"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_element = soup.find(id="render_today_price")
    if price_element:
        return price_element.text.strip()
    else:
        return None

def main():
    tn,py = st.columns(2)

    st.title("Fuel Price Tracker")
    st.markdown("""
    <style>
    .big-font {
        font-size:300px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    tn_petrol_price = fetch_tn_petrol_price()
    tn_diesel_price = fetch_tn_diesel_price()
    py_petrol_price = fetch_py_petrol_price()
    py_diesel_price = fetch_py_diesel_price()
    
    with tn:
        st.header("Tamil Nadu Prices",divider='green')
        st.write(f"Petrol Price:")
        tn_pp = st.empty()
        tn_pp.write(f"{tn_petrol_price}")
        st.divider()
        st.write(f"Diesel Price:")
        tn_pp = st.empty()
        tn_pp.write(f"{tn_diesel_price}")

    with py:
        st.header("Puducherry Prices",divider='green')
        st.write(f"Petrol Price:")
        tn_pp = st.empty()
        tn_pp.write(f"{py_petrol_price}")
        st.divider()
        st.write(f"Diesel Price:")
        tn_pp = st.empty()
        tn_pp.write(f"{py_diesel_price}")

    if tn_petrol_price:
        st.write(f"Today's Petrol Price in Chennai: {tn_petrol_price}")
    else:
        st.error("Failed to fetch petrol price. Please try again later.")
    
    if tn_diesel_price:
        st.write(f"Today's Diesel Price in Chennai: {tn_diesel_price}")
    else:
        st.error("Failed to fetch petrol price. Please try again later.")

if __name__ == "__main__":
    main()
