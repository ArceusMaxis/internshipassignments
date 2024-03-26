import streamlit as st
import requests
from bs4 import BeautifulSoup

def fetch_petrol_price():
    url = "https://www.businesstoday.in/fuel-price/petrol-price-in-chennai-today"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_element = soup.find(id="render_today_price")
    if price_element:
        return price_element.text.strip()
    else:
        return 
    
def fetch_diesel_price():
    url = "https://www.businesstoday.in/fuel-price/diesel-price-in-chennai-today"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_element = soup.find(id="render_today_price")
    if price_element:
        return price_element.text.strip()
    else:
        return None

def main():
    st.title("Tamil Nadu Fuel Prices Today")

    # Fetch petrol price
    petrol_price = fetch_petrol_price()
    diesel_price = fetch_diesel_price()

    # Display price
    if petrol_price:
        st.write(f"Today's Petrol Price in Chennai: {petrol_price}")
    else:
        st.error("Failed to fetch petrol price. Please try again later.")
    
    if diesel_price:
        st.write(f"Today's Diesel Price in Chennai: {diesel_price}")
    else:
        st.error("Failed to fetch petrol price. Please try again later.")

if __name__ == "__main__":
    main()
