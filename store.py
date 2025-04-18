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
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html {
            scroll-behavior: smooth;
        }
        
        body {
            font-family: 'Poppins', 'Segoe UI', Roboto, sans-serif;
            color: #f8f9fa;
            background: linear-gradient(-45deg, #0f2027, #203a43, #1a2a6c, #2c3e50);
            background-size: 400% 400%;
            animation: gradientBG 20s ease infinite;
            line-height: 1.6;
            min-height: 100vh;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            25% { background-position: 50% 100%; }
            50% { background-position: 100% 50%; }
            75% { background-position: 50% 0%; }
            100% { background-position: 0% 50%; }
        }
        
        .glass-effect {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        }
        
        .title {
            font-size: 3.8em;
            font-weight: 800;
            text-align: center;
            margin: 0.8em 0;
            background: linear-gradient(90deg, #f8f9fa, #00dbde, #fc00ff, #f8f9fa);
            background-size: 300% 300%;
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: titleGradient 8s ease infinite, float 6s ease-in-out infinite;
            padding: 0.3em;
            text-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
            letter-spacing: 2px;
        }

        @keyframes titleGradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        .stTextInput input {
            width: 100%;
            padding: 16px 25px;
            margin: 12px 0;
            border-radius: 50px;
            border: none;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.2), 0 10px 20px rgba(0, 0, 0, 0.15);
            color: white;
            font-size: 18px;
            font-weight: 500;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            animation: slideInDown 0.6s ease-out;
        }

        .stTextInput input:focus {
            background: rgba(255, 255, 255, 0.1);
            box-shadow: 0 0 25px rgba(131, 58, 180, 0.5), inset 0 0 10px rgba(0, 0, 0, 0.1);
            transform: translateY(-3px);
            outline: none;
        }
        
        .stTextInput input::placeholder {
            color: rgba(255, 255, 255, 0.6);
        }

        #MainMenu, footer, header {
            visibility: hidden;
        }
        
        .custom-button {
            display: inline-block;
            padding: 14px 28px;
            font-size: 16px;
            font-weight: 600;
            letter-spacing: 1px;
            color: #fff;
            background: linear-gradient(45deg, #833ab4, #fd1d1d, #fcb045);
            background-size: 200% 200%;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
            position: relative;
            overflow: hidden;
            z-index: 1;
            margin: 10px 15px;
            text-transform: uppercase;
        }

        .custom-button:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, #833ab4, #fd1d1d, #fcb045);
            background-size: 200% 200%;
            opacity: 0;
            transition: opacity 0.5s ease;
            z-index: -1;
            animation: gradientShift 3s ease infinite;
        }

        .custom-button:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
        }

        .custom-button:hover:before {
            opacity: 1;
        }

        .custom-button:active {
            transform: translateY(2px);
            box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .center-buttons {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
            margin: 30px 0;
        }

        .product-box {
            display: flex;
            flex-direction: column;
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 30px;
            background: rgba(20, 30, 48, 0.7);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
            transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        @media (min-width: 768px) {
            .product-box {
                flex-direction: row;
            }
        }

        .product-box:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
            background: rgba(30, 40, 58, 0.8);
        }

        @keyframes reveal {
            0% { opacity: 0; transform: translateY(30px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        .product-image {
            flex: 1;
            margin-right: 0;
            margin-bottom: 20px;
            position: relative;
            overflow: hidden;
            border-radius: 15px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
            animation: reveal 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }

        @media (min-width: 768px) {
            .product-image {
                margin-right: 25px;
                margin-bottom: 0;
            }
        }

        .product-image img {
            width: 100%;
            height: auto;
            border-radius: 12px;
            transition: transform 0.8s cubic-bezier(0.165, 0.84, 0.44, 1);
            object-fit: cover;
        }

        .product-image:hover img {
            transform: scale(1.15) rotate(2deg);
        }

        .product-image::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(to top, rgba(0,0,0,0.5), transparent);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .product-image:hover::after {
            opacity: 1;
        }

        .product-info {
            flex: 3;
            animation: reveal 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) 0.2s both;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .product-info h3 {
            margin: 0 0 15px 0;
            font-size: 1.8em;
            font-weight: 700;
            color: #fff;
            letter-spacing: 0.5px;
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            background: linear-gradient(90deg, #fff, #f0f0f0);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .product-info p {
            font-size: 1.2em;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 20px;
            font-weight: 500;
        }

        .product-info p strong {
            color: #64ffda;
            font-weight: 600;
        }

        .ebay-link {
            display: inline-block;
            background: linear-gradient(45deg, #4158D0, #C850C0, #FFCC70);
            background-size: 200% 200%;
            color: white;
            padding: 14px 28px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            letter-spacing: 1px;
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
            position: relative;
            overflow: hidden;
            align-self: flex-start;
            animation: gradientShift 3s ease infinite;
            text-transform: uppercase;
            font-size: 14px;
        }

        .ebay-link:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
            background-position: right center;
        }

        .ebay-link:active {
            transform: translateY(2px);
            box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
        }

        .ebay-link::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: 0.5s;
        }

        .ebay-link:hover::before {
            left: 100%;
        }

        .pagination-btn {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 50px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
        }

        .pagination-btn:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-3px);
            box-shadow: 0 12px 20px rgba(0, 0, 0, 0.3);
        }

        .pagination-btn:active {
            transform: translateY(0);
        }

        .stSpinner > div {
            border-color: #64ffda transparent transparent transparent !important;
        }

        hr {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            border: none;
            margin: 30px 0;
        }

        .stSuccess {
            background: rgba(100, 255, 218, 0.1) !important;
            color: #64ffda !important;
            border-radius: 10px !important;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(100, 255, 218, 0.2) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            animation: fadeInUp 0.5s ease-out;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .caption-text {
            font-size: 0.9em;
            text-align: center;
            color: rgba(255, 255, 255, 0.7);
            margin-top: 5px;
            font-style: italic;
        }

        .stButton button {
            border-radius: 50px !important;
            border: none !important;
            padding: 0.6em 1.5em !important;
            font-weight: 600 !important;
            background: linear-gradient(45deg, #833ab4, #fd1d1d, #fcb045) !important;
            background-size: 200% 200% !important;
            color: white !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3) !important;
            animation: gradientShift 3s ease infinite !important;
        }

        .stButton button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4) !important;
        }

        .stButton button:active {
            transform: translateY(0) !important;
            box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2) !important;
        }

        .stImage img {
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
            transition: all 0.5s ease;
        }

        .stImage img:hover {
            transform: scale(1.02);
        }

        .page-indicator {
            background: rgba(255, 255, 255, 0.1);
            padding: 8px 15px;
            border-radius: 50px;
            font-size: 14px;
            color: white;
            margin: 0 auto;
            text-align: center;
            width: fit-content;
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        }

        .no-results {
            text-align: center;
            padding: 50px 0;
            color: rgba(255, 255, 255, 0.7);
            font-size: 1.5em;
            font-weight: 300;
            letter-spacing: 1px;
        }

        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(45deg, #833ab4, #fd1d1d);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(45deg, #fd1d1d, #833ab4);
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
    price_str = price_str.replace('$', '').replace(',', '')
    
    match = re.search(r'\d+\.\d+', price_str)
    if match:
        return float(match.group())
    return 0.0  

def sort_products(products, sort_option):
    if sort_option == "The Cheapest":
        products['price_numeric'] = products['price'].apply(extract_price)
        products = products.sort_values(by='price_numeric', ascending=True)
    elif sort_option == "The Most Expensive":
        products['price_numeric'] = products['price'].apply(extract_price)
        products = products.sort_values(by='price_numeric', ascending=False)
    return products

def cleanup_database(database='products.db'):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS products')  # Only delete the products table
    conn.commit()
    conn.close()
    print(f"Deleted products table in database: {database}")

def initialize_database(database='products.db'):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    # Create the 'products' table
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                      link TEXT, 
                      title TEXT, 
                      price TEXT, 
                      img TEXT)''')
    # Create the 'account' table
    cursor.execute('''CREATE TABLE IF NOT EXISTS account (
                      email TEXT PRIMARY KEY, 
                      name TEXT, 
                      password TEXT)''')
    conn.commit()
    conn.close()

def account_creation_form():
    # Add a return button at the top-left corner
    if st.button("🔙", key="return_signup", help="Return to main page", use_container_width=True):
        st.session_state.view = "main"

    st.markdown('<div class="glass-effect" style="padding: 30px; margin: 20px 0;">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center;">Create an Account</h3>', unsafe_allow_html=True)
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    name = st.text_input("Name", placeholder="Enter your name")
    if st.button("Sign Up"):
        if email and password and name:
            conn = sqlite3.connect('products.db')
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM account WHERE email = ?", (email,))
            if cursor.fetchone():
                st.error("This email is already registered. Please sign in.")
            else:
                cursor.execute("INSERT INTO account (email, name, password) VALUES (?, ?, ?)", (email, name, password))
                conn.commit()
                st.success(f"Account created for {name} ({email})!")
                st.session_state.view = "main"  # Redirect to main page
            conn.close()
        else:
            st.error("Please fill in all fields.")
    st.markdown('</div>', unsafe_allow_html=True)

def sign_in_form():
    # Add a return button at the top-left corner
    if st.button("🔙", key="return_signin", help="Return to main page", use_container_width=True):
        st.session_state.view = "main"

    st.markdown('<div class="glass-effect" style="padding: 30px; margin: 20px 0;">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center;">Sign In</h3>', unsafe_allow_html=True)
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    if st.button("Sign In"):
        if email and password:
            conn = sqlite3.connect('products.db')
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM account WHERE email = ?", (email,))
            result = cursor.fetchone()
            if result is None:
                st.error("Account not found.")
            elif result[0] != password:
                st.error("Wrong password.")
            else:
                st.success(f"Welcome back, {email}!")
                st.session_state.view = "main"  # Redirect to main page
            conn.close()
        else:
            st.error("Please fill in all fields.")
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide", page_title="Modern Online Shop", page_icon="🛍️")
    apply_custom_css()
    
    st.markdown('<div class="title">🛍️ Modern Online Shop 🛍️</div>', unsafe_allow_html=True)

    # Add navigation buttons for account management
    st.markdown('<div class="center-buttons" style="gap: 10px;">', unsafe_allow_html=True)
    if st.button("👤 Sign Up", key="signup"):
        st.session_state.view = "signup"
    if st.button("🔑 Sign In", key="signin"):
        st.session_state.view = "signin"
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("view") == "signup":
        account_creation_form()
        return

    if st.session_state.get("view") == "signin":
        sign_in_form()
        return

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", use_container_width=True)
        st.markdown('<p class="caption-text">🐍 Powered by Python 🐍</p>', unsafe_allow_html=True)

    st.markdown('<div class="glass-effect" style="padding: 30px; margin: 20px 0;">', unsafe_allow_html=True)
    search_query = st.text_input("", value="", max_chars=None, placeholder='Search for products...', key='searchbox', help='Search in eBay 🔎')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="center-buttons">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("The Cheapest", key="cheapest"):
            st.session_state.sort_option = "The Cheapest"
    with col2:
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

    sort_option = st.session_state.get('sort_option', "Default")
    if sort_option != "Default":
        products = sort_products(products, sort_option)

    if products.empty:
        st.markdown('<div class="no-results">No products found. Try a different search!</div>', unsafe_allow_html=True)
    else:
        items_per_page = 4
        total_pages = max((len(products) + items_per_page - 1) // items_per_page, 1)
        page_number = st.session_state.get('page_number', 1)

        st.markdown(f'<div class="page-indicator">Page {page_number} of {total_pages}</div>', unsafe_allow_html=True)

        start_idx = (page_number - 1) * items_per_page
        end_idx = start_idx + items_per_page
        
        for idx in range(start_idx, min(end_idx, len(products))):
            product = products.iloc[idx]
            st.markdown(f'''
                <div class="product-box">
                    <div class="product-image">
                        <img src="{product['img']}" width="100%">
                    </div>
                    <div class="product-info">
                        <h3>{product['title']}</h3>
                        <p><strong>Price:</strong> {product['price']}</p>
                        <a target="_blank" href="{product['link']}" class="ebay-link">View on eBay</a>
                    </div>
                </div>
            ''', unsafe_allow_html=True)

        st.markdown('<div class="center-buttons">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if page_number > 1:
                if st.button("◀ Previous", key="prev"):
                    st.session_state.page_number = page_number - 1
        
        with col2:
            st.markdown(f'<div style="text-align: center; margin-top: 10px;">Page {page_number} of {total_pages}</div>', unsafe_allow_html=True)
            
        with col3:
            if page_number < total_pages:
                if st.button("Next ▶", key="next"):
                    st.session_state.page_number = page_number + 1
        st.markdown('</div>', unsafe_allow_html=True)
    
    socials = [
        {"name": "Telegram", "url": "https://t.me/mehrdad87org", "icon": "https://img.icons8.com/?size=100&id=k4jADXhS5U1t&format=png&color=000000", "class": "telegram"},
        {"name": "WhatsApp", "url": "https://wa.link/78c7u1", "icon": "https://img.icons8.com/?size=100&id=A1JUR9NRH7sC&format=png&color=000000", "class": "whatsapp"},
        {"name": "GitHub", "url": "https://github.com/mehrdad87org", "icon": "https://img.icons8.com/?size=100&id=LoL4bFzqmAa0&format=png&color=000000", "class": "github"},
        {"name": "Email", "url": "mailto:mehrdad87ourangg@gmail.com", "icon": "https://img.icons8.com/?size=100&id=eFPBXQop6V2m&format=png&color=000000", "class": "email"},
        {"name": "Instagram", "url": "https://instagram.com/mehrdad_ourang87", "icon": "https://img.icons8.com/?size=100&id=nj0Uj45LGUYh&format=png&color=000000", "class": "instagram"},
        {"name": "LinkedIn", "url": "https://www.linkedin.com/in/mehrdad-ourang-4204b734a", "icon": "https://img.icons8.com/?size=100&id=MR3dZdlA53te&format=png&color=000000", "class": "linkedin"}
    ]
    
    social_icons_html = ""
    for social in socials:
        social_icons_html += f'<a href="{social["url"]}" target="_blank" class="social-icon {social["class"]}"><img src="{social["icon"]}" width="40" height="40" alt="{social["name"]}"></a>'
    
    st.markdown('''
    <style>
        .footer {
            background: rgba(20, 30, 48, 0.8);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding: 30px 20px;
            margin-top: 50px;
            text-align: center;
            border-radius: 15px;
            box-shadow: 0 -10px 20px rgba(0, 0, 0, 0.1);
        }
        
        .footer p {
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 20px;
            font-size: 14px;
        }
        
        .footer a {
            color: #64ffda;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .footer a:hover {
            color: white;
        }
        
        .social-icons {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
            margin-top: 20px;
        }
        
        .social-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.05);
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }
        
        .social-icon:hover {
            transform: translateY(-5px) scale(1.1);
            background: rgba(255, 255, 255, 0.1);
            box-shadow: 0 15px 25px rgba(0, 0, 0, 0.3);
        }
        
        .social-icon img {
            transition: transform 0.3s ease;
        }
        
        .social-icon:hover img {
            transform: scale(1.2);
        }
        
        .telegram:hover { background: linear-gradient(45deg, #0088cc, #0099e6); }
        .whatsapp:hover { background: linear-gradient(45deg, #25d366, #128c7e); }
        .github:hover { background: linear-gradient(45deg, #333333, #5c5c5c); }
        .email:hover { background: linear-gradient(45deg, #ea4335, #fbbc05); }
        .instagram:hover { background: linear-gradient(45deg, #e1306c, #c13584, #833ab4, #fd1d1d, #f56040, #fcaf45); }
        .linkedin:hover { background: linear-gradient(45deg, #0077b5, #00a0dc); }
    </style>
    ''', unsafe_allow_html=True)
    
    # Add the footer to the page
    st.markdown(f'''
        <div class="footer">
            <p>© 2025 Modern Online Shop. All rights reserved. | <a href="#">Privacy Policy</a> | <a href="#">Terms of Service</a></p>
            <div class="social-icons">
                {social_icons_html}
            </div>
        </div>
    ''', unsafe_allow_html=True)

if __name__ == "__main__":
    initialize_database()  # Initialize the database before running the app
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 1
    if 'sort_option' not in st.session_state:
        st.session_state.sort_option = "Default"
    if 'view' not in st.session_state:
        st.session_state.view = "main"
    main()
