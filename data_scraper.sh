#!/bin/bash

#URL="https://www.veracash.com/gold-price-and-chart"
URL="https://atkinsonsbullion.com/charting"

DATA_FILE="/home/ubuntu/Data-Scraping-Dashboard-Project/gold_prices.csv"

# Fetch the webpage content and save it to a temporary file
curl -s "$URL" > temp.html

# Extract the $ price then isolate just the numeric portion 
PRICE=$(grep -oP '\$[ \t]*[0-9,]+\.[0-9]+\s*/\s*oz' temp.html | sed -E 's/\$[[:space:]]*//; s/\/[[:space:]]*oz//; s/,//g')


# Get the current timestamp
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Add the date and price to the data file
echo "$TIMESTAMP,$PRICE" >> "$DATA_FILE"

echo "Scraped price: $PRICE"

rm temp.html
