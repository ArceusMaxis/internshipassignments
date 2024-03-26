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
        return None

def main():
    st.title("Chennai Petrol Price Today")

    # Fetch petrol price
    petrol_price = fetch_petrol_price()

    # Display price
    if petrol_price:
        st.write(f"Today's Petrol Price in Chennai: {petrol_price}")
    else:
        st.error("Failed to fetch petrol price. Please try again later.")

if __name__ == "__main__":
    main()
