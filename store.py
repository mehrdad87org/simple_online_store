import streamlit as st
import sqlite3
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os
import atexit

def apply_custom_css():
    custom_css = """
    <style>
        /* General Styles */
        body {
            font-family: 'Arial', sans-serif;
            color: white;
            background: linear-gradient(-45deg, #001933, #003366, #004080, #00509e);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Title Animation */
        .title {
            font-size: 3.5em;
            font-weight: bold;
            text-align: center;
            animation: typing 3s steps(40, end), blink-caret 0.75s step-end infinite, glow 2s ease-in-out infinite;
            white-space: nowrap;
            overflow: hidden;
            border-right: 0.15em solid orange;
        }

        @keyframes typing {
            from { width: 0; }
            to { width: 100%; }
        }

        @keyframes blink-caret {
            from, to { border-color: transparent; }
            50% { border-color: orange; }
        }

        @keyframes glow {
            0%, 100% { text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 20px #ff9d00, 0 0 40px #ff9d00; }
            50% { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 40px #ff9d00, 0 0 80px #ff9d00; }
        }

        /* Custom Search Box */
        .stTextInput input {
            width: 100%;
            padding: 12px 20px;
            margin: 8px 0;
            box-sizing: border-box;
            border: 2px solid #007BFF;
            border-radius: 25px;
            background-color: rgba(0, 0, 0, 0.5);
            color: white;
            font-size: 16px;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
            animation: slideInLeft 0.5s ease-in-out;
        }

        .stTextInput input:focus {
            border-color: #00ff88;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.5);
            outline: none;
        }

        .stTextInput input:hover {
            border-color: #00ff88;
        }

        /* Custom Button Styles */
        .custom-button {
            display: inline-block;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: bold;
            color: black; /* Black text */
            background-color: #FFD700; /* Yellow */
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
            animation: fadeIn 0.5s ease-in-out;
            margin: 10px;
        }

        .custom-button:hover {
            background-color: #FFC300; /* Darker yellow on hover */
            transform: translateY(-3px);
            box-shadow: 0 0 15px rgba(255, 195, 0, 0.5);
        }

        .custom-button:active {
            transform: translateY(0);
            animation: pulse 0.5s;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }

        /* Center Buttons */
        .center-buttons {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
        }

        /* Product Box Styles */
        .product-box {
            display: flex;
            border: 1px solid #444;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            background-color: rgba(0, 0, 0, 0.5);
            transition: transform 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease;
            animation: fadeIn 0.5s ease-in-out, float 4s ease-in-out infinite;
        }

        .product-box:hover {
            transform: scale(1.02);
            box-shadow: 0 0 20px rgba(0, 123, 255, 0.5);
            background-color: rgba(0, 0, 0, 0.7);
        }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        .product-image {
            flex: 1;
            margin-right: 20px;
            animation: slideInLeft 0.5s ease-in-out, zoomIn 0.5s ease-in-out;
        }

        .product-image img {
            border-radius: 10px;
            transition: transform 0.3s ease;
        }

        .product-image img:hover {
            transform: scale(1.1);
        }

        @keyframes zoomIn {
            from { transform: scale(0.9); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }

        .product-info {
            flex: 3;
            animation: slideInRight 0.5s ease-in-out;
        }

        .product-info h3 {
            margin-top: 0;
            font-size: 1.5em;
            color: white;
            animation: fadeIn 0.5s ease-in-out;
        }

        .product-info p {
            font-size: 1.1em;
            color: white;
            animation: fadeIn 0.5s ease-in-out;
        }

        .ebay-link {
            display: inline-block;
            background-color: #007BFF;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            text-decoration: none;
            transition: background-color 0.3s ease, transform 0.3s ease;
            animation: fadeIn 0.5s ease-in-out;
        }

        .ebay-link:hover {
            background-color: #0056b3;
            transform: translateY(-3px);
            animation: pulse 1s infinite;
        }

        .ebay-link:active {
            transform: translateY(0);
        }

        /* Keyframe Animations */
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }

        @keyframes slideInLeft {
            from {
                transform: translateX(-20px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        @keyframes slideInRight {
            from {
                transform: translateX(20px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        @keyframes bounceIn {
            0% {
                transform: scale(0.5);
                opacity: 0;
            }
            60% {
                transform: scale(1.1);
                opacity: 1;
            }
            100% {
                transform: scale(1);
            }
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def fetch_html(url):
    headers = {
        "User-Agent": "Your User Agent",
        "Accept-Language": "en-US, en;q=0.5"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.content

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find_all("div", class_="s-item__info")
    images = soup.find_all("div", class_="s-item__image-wrapper image-treatment")
    
    items = []
    for product, img in zip(products, images):
        title = product.select_one('.s-item__title').text if product.select_one('.s-item__title') else "N/A"
        link = product.select_one('.s-item__link')['href'] if product.select_one('.s-item__link') else "N/A"
        price = product.select_one('.s-item__price').text if product.select_one('.s-item__price') else "N/A"
        img_tag = img.find("img")
        img_url = img_tag['src'] if img_tag else "N/A"
        items.append((link, title, price, img_url))
    return items

def store_data(database, data):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS products')  

    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                      link TEXT, 
                      title TEXT, 
                      price TEXT, 
                      img TEXT)''')

    data = data[2:]  
    if data:
        data = [data[0]] + data  
        cursor.executemany('INSERT INTO products (link, title, price, img) VALUES (?,?,?,?)', data)
    conn.commit()
    conn.close()

def fetch_product_data(database='products.db'):
    conn = sqlite3.connect(database)
    query = '''SELECT link, title, price, img FROM products'''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def extract_price(price_str):
    """
    Extract the minimum price from a price string (handles ranges like "166.95 to 198.95").
    """
    
    price_str = price_str.replace('$', '').replace(',', '')
    
    match = re.search(r'\d+\.\d+', price_str)
    if match:
        return float(match.group())
    return 0.0  

def sort_products(products, sort_option):
    """
    Sort products based on the selected option.
    """
    if sort_option == "The Cheapest":
        
        products['price_numeric'] = products['price'].apply(extract_price)
        products = products.sort_values(by='price_numeric', ascending=True)
    elif sort_option == "The Most Expensive":
        
        products['price_numeric'] = products['price'].apply(extract_price)
        products = products.sort_values(by='price_numeric', ascending=False)
    return products

def cleanup_database(database='products.db'):
    """
    Delete the database file when the script exits.
    """
    if os.path.exists(database):
        os.remove(database)
        print(f"Deleted database file: {database}")


atexit.register(cleanup_database)

def main():
    st.set_page_config(layout="centered")
    apply_custom_css()  # Apply custom CSS
    st.markdown('<div class="title">🌐 Online Store 🌐</div>', unsafe_allow_html=True)

    st.image("logo.png", use_container_width=True, caption='🐍 Python Programming 🐍')

    
    search_query = st.text_input("Search in eBay 🔎", value="", max_chars=None, placeholder='Search in eBay', key='searchbox', label_visibility='collapsed', help='Search in eBay 🔎').strip()

    # Centered buttons under the search box
    st.markdown('<div class="center-buttons">', unsafe_allow_html=True)
    if st.button("The Cheapest", key="cheapest"):
        st.session_state.sort_option = "The Cheapest"
    if st.button("The Most Expensive", key="most_expensive"):
        st.session_state.sort_option = "The Most Expensive"
    st.markdown('</div>', unsafe_allow_html=True)

    if search_query:
        with st.spinner("Fetching data from eBay...🔎"):
            base_url = "https://www.ebay.com/sch/i.html?_nkw="
            url = f"{base_url}{search_query}"
            html = fetch_html(url)
            products = parse_html(html)
            store_data('products.db', products)
            st.success("✅ Data fetched successfully ✅")
    
    try:
        products = fetch_product_data()
    except pd.io.sql.DatabaseError:
        products = pd.DataFrame(columns=['link', 'title', 'price', 'img']) 

    # Sort products based on the selected option
    sort_option = st.session_state.get('sort_option', "Default")
    if sort_option != "Default":
        products = sort_products(products, sort_option)

    
    items_per_page = 4
    total_pages = max((len(products) + items_per_page - 1) // items_per_page, 1)
    page_number = st.session_state.get('page_number', 1)

    start_idx = (page_number - 1) * items_per_page
    end_idx = start_idx + items_per_page

    
    if not products.empty:
        for idx in range(start_idx, min(end_idx, len(products))):
            product = products.iloc[idx]
            st.markdown(f'''
                <div class="product-box">
                    <div class="product-image">
                        <img src="{product['img']}" width="200">
                    </div>
                    <div class="product-info">
                        <h3>{product['title']}</h3>
                        <p><strong>Price:</strong> {product['price']}</p>
                        <a target="_blank" href="{product['link']}" class="ebay-link">View on eBay</a>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            st.write("---")  

    st.write("") 

   
    st.markdown('<div class="center-buttons">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if page_number > 1 and st.button("◀ Previous Page", key="prev"):
            st.session_state.page_number = page_number - 1
    with col2:
        if page_number < total_pages and st.button("Next Page ▶", key="next"):
            st.session_state.page_number = page_number + 1
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")  

if __name__ == "__main__":
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 1
    if 'sort_option' not in st.session_state:
        st.session_state.sort_option = "Default"
    main()
