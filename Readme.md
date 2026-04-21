# IMDb Top 250 Scraper & Analyzer

A Python project that scrapes the [IMDb Top 250 Movies](https://www.imdb.com/chart/top/) list and performs data analysis with visualizations.

---

## Project Structure

```
├── src/
│   ├── Main.py               # Entry point — runs the full pipeline
│   ├── Scrape.py             # Selenium-based web scraper
│   └── Analysis.py           # Data analysis & chart generation
│
├── data/
│   ├── imdb_top250.csv       # Scraped data (CSV)
│   ├── imdb_top250.xlsx      # Scraped data (Excel)
│   └── imdb_top250.json      # Scraped data (JSON)
│
├── charts/
│   ├── rating_distribution.png
│   ├── top_10_movies.png
│   ├── rating_vs_year.png
│   └── avg_rating_by_decade.png
│
├── .gitignore
└── README.md
```

---

## Features

- **Web Scraping** — Headless Selenium scraper that handles JavaScript-rendered IMDb pages, with automatic retry logic (up to 3 attempts)
- **Multi-format Export** — Saves scraped data as CSV, Excel (.xlsx), and JSON
- **Data Analysis** — Summary statistics using Pandas (rating range, year range, totals)
- **Visualizations** — Four Matplotlib charts:
  - Rating distribution histogram
  - Top 10 movies by IMDb rating (horizontal bar chart)
  - IMDb rating vs. release year (scatter plot)
  - Average rating by decade (line chart)

---

## Tech Stack

| Tool        | Purpose                  |
|-------------|--------------------------|
| Python 3    | Core language            |
| Selenium    | Web scraping             |
| Pandas      | Data processing          |
| Matplotlib  | Data visualization       |
| OpenPyXL    | Excel export             |

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/imdb-top250.git
cd imdb-top250
```

### 2. Install dependencies
```bash
pip install selenium pandas matplotlib openpyxl
```

> Make sure you have [ChromeDriver](https://chromedriver.chromium.org/downloads) installed and available in your PATH.

### 3. Run the pipeline
```bash
python src/Main.py
```

This will:
1. Scrape the IMDb Top 250 page
2. Export data to `data/imdb_top250.csv`, `.xlsx`, and `.json`
3. Generate all four charts inside the `charts/` folder

---

## Sample Output

The dataset contains fields for each movie:

| rank | title                    | year | duration | imdb_rating |
|------|--------------------------|------|----------|-------------|
| 1    | The Shawshank Redemption | 1994 | 2h 22m   | 9.3         |
| 2    | The Godfather            | 1972 | 2h 55m   | 9.2         |
| 3    | The Dark Knight          | 2008 | 2h 32m   | 9.1         |

---

## License

This project is for educational purposes only. Data is sourced from [IMDb](https://www.imdb.com).