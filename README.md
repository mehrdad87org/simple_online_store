# Online Shop Scraper and Viewer

This is a Python-based web application that scrapes product data from eBay, stores it in a SQLite database, and displays it in a user-friendly interface using Streamlit. The application allows users to search for products, sort them by price, and view them in a paginated format.

## Features

- **Web Scraping**: Fetches product data (title, price, image, and link) from eBay based on a user-provided search query.
- **Database Storage**: Stores scraped data in a SQLite database for quick retrieval.
- **Custom UI**: Displays products in a visually appealing format with custom CSS styling.
- **Sorting**: Allows users to sort products by price (cheapest or most expensive).
- **Pagination**: Displays products in a paginated manner for better navigation.
- **Responsive Design**: The interface is designed to be responsive and user-friendly.

## Technologies Used

- **Python**: The core programming language used for the application.
- **Streamlit**: Used to create the web interface.
- **SQLite**: Used to store and retrieve product data.
- **BeautifulSoup**: Used for parsing HTML and extracting product information.
- **Requests**: Used to fetch HTML content from eBay.
- **Pandas**: Used for data manipulation and database querying.

## How It Works

1. **User Input**: The user enters a search query in the search box.
2. **Web Scraping**: The application fetches the HTML content of the eBay search results page.
3. **Data Parsing**: The HTML content is parsed to extract product details (title, price, image, and link).
4. **Database Storage**: The extracted data is stored in a SQLite database.
5. **Data Display**: The stored data is retrieved and displayed in a paginated format.
6. **Sorting**: Users can sort the products by price (cheapest or most expensive).
7. **Pagination**: Users can navigate through multiple pages of products.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mehrdad87org/simple_online_store.git
   cd simple_online_store

Install Dependencies:
pip install -r requirements.txt
Run the Application:
streamlit run store.py
