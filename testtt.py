# url = "http://dev.bootcamp.store.supersqa.com/",
# consumer_key = "ck_8169f43e770dc493cae77d7828e227835284050c",
# consumer_secret = "cs_581ae674c7298f39cf75d30523eb235b25bad1db",
# version = "wc/v3"

import requests
import argparse
import csv

# Function to fetch all products from WooCommerce API
def get_all_products(url, consumer_key, consumer_secret):
    all_products = []
    page = 1
    per_page = 100
    while True:
        # Make the API call to retrieve products
        response = requests.get(
            f"http://dev.bootcamp.store.supersqa.com/wp-json/wc/v3/products",
            params={"consumer_key": "ck_8169f43e770dc493cae77d7828e227835284050c", "consumer_secret": "cs_581ae674c7298f39cf75d30523eb235b25bad1db", "page": page, "per_page": per_page}
        )
        if response.status_code == 200:
            products = response.json()
            if len(products) == 0:
                break
            all_products.extend(products)
            page += 1
        else:
            print("Error fetching products:", response.text)
            break
    return all_products

# Function to filter products by price
def filter_products_by_price(products, max_price):
    filtered_products = [product for product in products if float(product['price']) < max_price]
    return filtered_products

# Function to print products under a certain price
def print_products_under_price(products):
    if not products:
        print("No products found under the specified price.")
    else:
        print("Products under the specified price:")
        for product in products:
            print(f"{product['name']} - Price: ${product['price']}")

# Function to save products to CSV file
def save_to_csv(products, filename):
    if not products:
        print("No products to save to CSV.")
    else:
        with open(filename, mode='w', newline='') as file:
            fieldnames = ['Product Name', 'Price']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for product in products:
                writer.writerow({'Product Name': product['name'], 'Price': product['price']})

# Parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Get products priced under a certain amount from WooCommerce.')
    parser.add_argument('--url', type=str, default='http://dev.bootcamp.store.supersqa.com/', help='WooCommerce website URL')
    parser.add_argument('--consumer_key', type=str, default='ck_8169f43e770dc493cae77d7828e227835284050c', help='WooCommerce API Consumer Key')
    parser.add_argument('--consumer_secret', type=str, default='cs_581ae674c7298f39cf75d30523eb235b25bad1db', help='WooCommerce API Consumer Secret')
    parser.add_argument('--price_cut', type=float, help='Maximum price for filtering products')
    parser.add_argument('--output_file', type=str, default='filtered_products.csv', help='Output CSV file name')
    return parser.parse_args()

# Main function
def main():
    # Parse command-line arguments
    args = parse_arguments()

    # WooCommerce API credentials and URL
    url = args.url
    consumer_key = args.consumer_key
    consumer_secret = args.consumer_secret

    # Fetch all products from WooCommerce
    all_products = get_all_products(url, consumer_key, consumer_secret)

    # Filter products by price
    max_price = args.price_cut if args.price_cut else 10  # Default maximum price is $10
    filtered_products = filter_products_by_price(all_products, max_price)

    # Print products under the specified price to console
    print_products_under_price(filtered_products)

    # Save filtered products to CSV
    filename = args.output_file
    save_to_csv(filtered_products, filename)

if __name__ == "__main__":
    main()
