# Online Store - eBay Product Search and Display

This project is a Streamlit-based web application that allows users to search for products on eBay and display the results in an interactive and visually appealing interface. The application fetches product data from eBay, stores it in a SQLite database, and displays the products with options to sort and paginate through the results.

## Features

1. **Search Products on eBay**:
   - Users can enter a search query to fetch products from eBay.
   - The application uses web scraping to extract product details such as title, price, image, and link.

2. **Sort Products**:
   - Users can sort the products by price:
     - "The Cheapest": Sorts products from lowest to highest price.
     - "The Most Expensive": Sorts products from highest to lowest price.

3. **Pagination**:
   - Products are displayed in pages, with 4 products per page.
   - Users can navigate between pages using "Previous Page" and "Next Page" buttons.

4. **Custom Styling**:
   - The application uses custom CSS for a modern and animated user interface.
   - Features include neon title animations, gradient backgrounds, and hover effects.

5. **Database Integration**:
   - Product data is stored in a SQLite database (`products.db`).
   - The database is cleaned up (deleted) when the application exits.

6. **Responsive Design**:
   - The application is designed to be responsive and works well on different screen sizes.

7. **Social Media Links**:
   - The footer includes links to social media profiles and contact information.

## How It Works

1. **Search Query**:
   - The user enters a search query in the input box.
   - The application constructs a URL to search for the query on eBay.

2. **Web Scraping**:
   - The application fetches the HTML content of the eBay search results page.
   - It uses BeautifulSoup to parse the HTML and extract product details.

3. **Database Storage**:
   - Extracted product data is stored in a SQLite database for quick access and sorting.

4. **Display Products**:
   - Products are displayed in a grid format with images, titles, prices, and links to eBay.
   - Users can sort the products by price and navigate through pages.

5. **Custom CSS**:
   - The application applies custom CSS styles for animations, hover effects, and a visually appealing design.

## Requirements

- Python 3.x
- Streamlit (`pip install streamlit`)
- BeautifulSoup (`pip install beautifulsoup4`)
- Requests (`pip install requests`)
- Pandas (`pip install pandas`)
- SQLite3 (included in Python standard library)
