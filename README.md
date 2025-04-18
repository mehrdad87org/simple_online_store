# Modern Online Shop

Modern Online Shop is a Streamlit-based web application that allows users to search for products on eBay, sort them by price, and manage user accounts with sign-up and sign-in functionality.

## Features

- **Product Search**: Search for products on eBay using keywords.
- **Sorting Options**: Sort products by "The Cheapest" or "The Most Expensive".
- **User Accounts**: 
  - Sign up with email, name, and password.
  - Prevent duplicate email registration.
  - Sign in with email and password.
  - Error handling for incorrect email or password.
- **Responsive Design**: Modern UI with a responsive layout.
- **Database Management**: 
  - Stores user accounts persistently.
  - Deletes the `products` table upon exiting the application.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/modern-online-shop.git
   cd modern-online-shop
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run store.py
   ```

## Usage

1. **Search Products**: Enter a keyword in the search bar to fetch products from eBay.
2. **Sort Products**: Use the "The Cheapest" or "The Most Expensive" buttons to sort the results.
3. **Sign Up**: Create an account by providing your email, name, and password.
4. **Sign In**: Log in with your email and password. If the email or password is incorrect, appropriate error messages will be displayed.
5. **Return to Main Page**: Use the green "🔙" button to return to the main page from the sign-up or sign-in pages.

## Requirements

- Python 3.7 or higher
- Internet connection (for fetching data from eBay)

## File Structure

- `store.py`: Main application file.
- `requirements.txt`: List of dependencies.
- `README.md`: Documentation.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author

Developed by Mehrdad Ourang.
