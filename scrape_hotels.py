# Use Booking.com to scrape US hotel prices to determine and rank which US States have the cheapest winter hotels.						

# Importing libraries
import requests  # To send HTTP requests.
from bs4 import BeautifulSoup  # For parsing HTML content.
import pandas as pd  # For handling data and creating a Dataframe.
import re  # For regular expressions to process the prices.


# Scraping function
def scrape_cheapest_price(location):
    url = f"https://www.booking.com/searchresults.html?ss={location}&checkin_monthday=15&checkin_year_month=2024-12&checkout_monthday=31&checkout_year_month=2024-12"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
# Added a User-Agent header to mimic a request from a web browser

    try:
        response = requests.get(url, headers=headers)  # Sends an HTTP GET request to the specified URL.
        response.raise_for_status()  # Checks if the request was successful.
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None  # If there's an error, it prints the error message and returns 'None'.

    soup = BeautifulSoup(response.text, 'html.parser')   # Parses the HTML content of the response using BeautifulSoup.

    # (Adjustable) this selector can change to match the price element in the HTML
    price_elements = soup.select('span[data-testid="price-and-discounted-price"]')

    # Loops through each price element found.
    prices = []

    for element in price_elements:
        try:
            price_text = element.get_text(strip=True)  # Extracts the text from the element.
            # Extracts numeric value from text in float format for accuracy.
            price_value = float(re.sub(r'[^\d.]', '', price_text))
            prices.append(price_value)
        except ValueError:
            continue

    if not prices:
        return None
    return min(prices) # Returns cheapest price


# List of states to scrape
states = ["New York", "California", "Texas", "Florida", "Nevada", "Arizona", "Michigan", "Ohio", "Illinois", "Georgia"]
results = []

for state in states:
    print(f"Scraping prices for {state}...")
    cheapest_price = scrape_cheapest_price(state)
    if cheapest_price is not None:
        results.append({"State": state, "Cheapest Price": cheapest_price})
    else:
        results.append({"State": state, "Cheapest Price": "N/A"})

# Save results to CSV
df = pd.DataFrame(results)
df.to_csv('cheapest_hotel_prices.csv', index=False)

# Print the results for verification
print(df)

