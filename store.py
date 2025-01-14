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
            font-family: Arial, sans-serif;
            color: white;
        }

        /* Product Box Styles */
        .product-box {
            display: flex;
            border: 1px solid #444;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            background-color: #001933; /* Darker blue */
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .product-box:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        .product-image {
            flex: 1;
            margin-right: 20px;
        }

        .product-info {
            flex: 3;
        }

        .product-info h3 {
            margin-top: 0;
            font-size: 1.5em;
            color: white;
        }

        .product-info p {
            font-size: 1.1em;
            color: white;
        }

        .ebay-link {
            display: inline-block;
            background-color: #007BFF;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            text-decoration: none;
            transition: background-color 0.3s;
        }

        .ebay-link:hover {
            background-color: #0056b3;
        }

        /* Slider Styles */
        .stSlider {
            margin: 20px 0;
        }

        /* Button Styles */
        .stButton button {
            background-color: #007BFF;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .stButton button:hover {
            background-color: #0056b3;
        }

        /* Circular Sort Buttons */
        .sort-button {
            display: inline-block;
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background-color: #FFD700; /* Yellow */
            color: black; /* Black text */
            text-align: center;
            line-height: 100px;
            font-size: 16px;
            cursor: pointer;
            margin: 5px;
            transition: background-color 0.3s;
        }

        .sort-button:hover {
            background-color: #FFC300; /* Darker yellow on hover */
        }

        .sort-button.active {
            background-color: #FFC300; /* Darker yellow for active state */
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
    apply_custom_css()  
    st.title("🌐 Online Shop 🌐")

    st.image("python.png", use_container_width=True, caption='🐍 Python Programming 🐍')

    # Search box
    search_query = st.text_input("Search in eBay 🔎", value="", max_chars=None, placeholder='Search in eBay', key='searchbox', label_visibility='collapsed', help='Search in eBay 🔎').strip()

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

    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("The Cheapest", key="cheapest"):
            st.session_state.sort_option = "The Cheapest"
    with col2:
        if st.button("The Most Expensive", key="most_expensive"):
            st.session_state.sort_option = "The Most Expensive"

    
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

   
    col_blank1, col_prev, col_next, col_blank2 = st.columns([1, 2, 2, 1])

    if total_pages > 1:
        page_number = st.slider("Page", 1, total_pages, page_number, key="slider")

    with col_prev:
        if page_number > 1 and st.button("◀ Previous Page", key="prev"):
            st.session_state.page_number = page_number - 1

    with col_next:
        if page_number < total_pages and st.button("Next Page ▶", key="next"):
            st.session_state.page_number = page_number + 1

    st.write("")  

if __name__ == "__main__":
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 1
    if 'sort_option' not in st.session_state:
        st.session_state.sort_option = "Default"
    main()
