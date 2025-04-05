# Data-Scraping-Dashboard-Project

# Gold Price Scraper & Dashboard

This project continuously scrapes live gold price data from a public website using a **Bash script** and displays it in a **Python Dash dashboard** with historical graphs and daily financial summaries.

## Project Overview

- **Live Scraping:** Retrieves the latest gold price from a target website every 5 minutes.
- **Bash-only Scraper:** Built entirely using Bash, `curl`, `grep`, `sed`, and `regex`.
- **Time-Series Dashboard:** Python Dash app visualizes price trends over time.
- **Daily Report:** Automatically generated at 8 PM with key metrics like:
  - Daily high / low
  - Open & close prices
  - Daily return
  - Volatility 

---
