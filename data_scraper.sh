#!/bin/bash

URL="https://www.veracash.com/gold-price-and-chart"

DATA_FILE="gold_prices.csv"

# Fetch the webpage content and save it to a temporary file
curl -s "$URL" > temp.html

# Extract "US$2,984.68 / oz" then isolate just the numeric portion 
PRICE=$(grep -oP 'US\$[0-9,]+\.[0-9]+\s*/\s*oz' temp.html | sed -E 's/US\$| \/ oz//g' | sed 's/,//g')


# Get the current timestamp
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Add the date and price to the data file
echo "$TIMESTAMP,$PRICE" >> "$DATA_FILE"

echo "Scraped price: $PRICE"

rm temp.html
