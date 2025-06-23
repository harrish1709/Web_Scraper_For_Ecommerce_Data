from bs4 import BeautifulSoup
import requests
import pandas as pd

SnapdealNames = []
SnapdealPrices = []
SnapdealRatings = []

text = input("Enter the Product you want to Search: ").strip()
searchText = text.replace(" ", "%20")  # URL-encode spaces
url = f"https://www.snapdeal.com/search?keyword={searchText}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')
except requests.exceptions.RequestException as e:
    print("Error fetching the webpage:", e)
    exit()

def Snapdeal():
    product_cards = soup.find_all("div", class_="product-tuple-listing")
    for card in product_cards:
        # Name
        name_tag = card.find("p", class_="product-title")
        name = name_tag.text.strip() if name_tag else "N/A"

        # Price
        price_tag = card.find("span", class_="product-price")
        price_text = price_tag.text.strip().replace("Rs. ", "").replace(",", "") if price_tag else "0"

        # Rating
        rating_tag = card.find("div", class_="filled-stars")
        if rating_tag:
            width_str = rating_tag.get("style").replace("width:", "").replace("%", "").strip()
            try:
                star_rating = round((float(width_str) / 100) * 5, 1)  # Convert percent to 5-star rating
                rating = f"{star_rating} ⭐"
            except:
                rating = "N/A"
        else:
            rating = "N/A"


        try:
            price = int(price_text)
            SnapdealNames.append(name)
            SnapdealPrices.append(price)
            SnapdealRatings.append(rating)
        except ValueError:
            continue

Snapdeal()

# Debug
print(f"Scraped {len(SnapdealNames)} products.")

# Ensure all lists are the same length
min_len = min(len(SnapdealNames), len(SnapdealPrices), len(SnapdealRatings))
SnapdealNames = SnapdealNames[:min_len]
SnapdealPrices = SnapdealPrices[:min_len]
SnapdealRatings = SnapdealRatings[:min_len]

# Combine and sort by price
combined_data = list(zip(SnapdealNames, SnapdealPrices, SnapdealRatings))
sorted_data = sorted(combined_data, key=lambda x: x[1])

# Create DataFrames
sheet1 = pd.DataFrame({
    'PRODUCT NAME': SnapdealNames,
    'PRODUCT PRICE': SnapdealPrices,
    'PRODUCT RATINGS': SnapdealRatings
})

sheet2 = pd.DataFrame({
    'PRODUCT NAME': [x[0] for x in sorted_data],
    'PRODUCT PRICE': [x[1] for x in sorted_data],
    'PRODUCT RATINGS': [x[2] for x in sorted_data],
})

# Export to Excel
sheet1.to_excel("Snapdeal_Unsorted.xlsx", sheet_name='ScrapedData', index=False)
sheet2.to_excel("Snapdeal_Sorted.xlsx", sheet_name='SortedData', index=False)

print("SCRAPING SUCCESSFUL ✅ Files saved: Snapdeal_Unsorted.xlsx, Snapdeal_Sorted.xlsx")
