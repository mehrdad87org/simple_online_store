# Modern Online Shop

A sleek, modern e-commerce web application built with Streamlit and Python that allows users to search and browse products from eBay.

![Modern Online Shop](logo.png)

## Features

- **Beautiful UI with Glass Morphism Design**: Modern user interface with glass effect, gradient animations, and responsive design
- **eBay Product Search**: Search for products directly from eBay
- **Product Sorting**: Sort products by price (cheapest/most expensive) or popularity
- **Favorites System**: Save products to your favorites list
- **Shopping Cart**: Add products to cart for later checkout
- **Pagination**: Browse through multiple pages of search results
- **Toast Notifications**: Receive confirmation of user actions
- **Responsive Design**: Works across desktop and mobile devices

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/modern-online-shop.git
   cd modern-online-shop
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   streamlit run store.py
   ```

## Usage

1. **Search for Products**: Enter a search term in the search box and press Enter
2. **Sort Results**: Click the sorting buttons to arrange products by price or popularity
3. **View Product Details**: Click on product cards to see more information
4. **Add to Favorites**: Click the heart icon to add a product to your favorites
5. **Add to Cart**: Click the cart icon or "Add to Cart" button to add products to your cart
6. **View Cart/Favorites**: Use the navigation menu to access your cart and favorites
7. **Checkout**: Navigate to your cart and click "Proceed to Checkout" to complete your purchase

## Technical Details

- **Web Scraping**: The application scrapes eBay search results using BeautifulSoup
- **Data Storage**: Product data is temporarily stored in an SQLite database
- **Session Management**: User cart and favorites are stored in Streamlit's session state
- **Interactive Elements**: The UI includes JavaScript for enhanced user interaction

## Dependencies

See [requirements.txt](requirements.txt) for a list of dependencies.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- eBay for product data
- Streamlit for the amazing web app framework
- Icons and graphics from various free sources
