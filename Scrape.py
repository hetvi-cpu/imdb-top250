from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import json


# ── Constants ─────────────────────────────────────────────────────────────────
URL         = "https://www.imdb.com/chart/top/"
MAX_RETRIES = 3
CSS_ROW     = 'li.ipc-metadata-list-summary-item'
CSS_TITLE   = 'h3.ipc-title__text'
CSS_META    = 'li.ipc-inline-list__item'
CSS_RATING  = 'span.ipc-rating-star--imdb'


# ── Browser setup ─────────────────────────────────────────────────────────────
def get_driver():
    return webdriver.Chrome()

# ── Page loader with retry ────────────────────────────────────────────────────
def load_page(driver):
    """Load IMDb Top 250 page, retrying up to MAX_RETRIES times."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            driver.get(URL)
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, CSS_ROW))
            )
            time.sleep(2)  # extra buffer for full JS render
            print(f"  Page loaded on attempt {attempt}")
            return True
        except Exception as e:
            print(f"  Attempt {attempt} failed: {e}")
            time.sleep(3)

    print("  Could not load IMDb after 3 attempts.")
    return False


# ── Row parser ────────────────────────────────────────────────────────────────
def parse_row(row, idx):
    """Extract movie data from a single list-item row. Returns dict or None."""
    try:
        raw_title = row.find_element(By.CSS_SELECTOR, CSS_TITLE).text
        title     = raw_title.split('. ', 1)[-1].strip()

        metadata = row.find_elements(By.CSS_SELECTOR, CSS_META)
        year     = metadata[0].text if len(metadata) > 0 else 'N/A'
        duration = metadata[1].text if len(metadata) > 1 else 'N/A'

        rating_el = row.find_elements(By.CSS_SELECTOR, CSS_RATING)
        rating    = rating_el[0].text.split()[0] if rating_el else 'N/A'

        return {
            'rank':        idx,
            'title':       title,
            'year':        year,
            'duration':    duration,
            'imdb_rating': rating
        }
    except Exception as e:
        print(f"  Row {idx} parse error: {e} — skipping")
        return None


# ── Data cleaner ──────────────────────────────────────────────────────────────
def clean_dataframe(movies):
    """Convert raw list of dicts into a clean, typed DataFrame."""
    df = pd.DataFrame(movies)
    df['year']        = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
    df['imdb_rating'] = pd.to_numeric(df['imdb_rating'], errors='coerce')
    df.drop_duplicates(subset=['title', 'year'], inplace=True)
    df.sort_values('rank', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


# ── Exporter ──────────────────────────────────────────────────────────────────
def export_data(df, movies):
    """Save DataFrame to CSV + Excel and raw list to JSON."""
    df.to_csv('imdb_top250.csv', index=False)
    df.to_excel('imdb_top250.xlsx', index=False)
    with open('imdb_top250.json', 'w') as f:
        json.dump(movies, f, indent=2)
    print(f"  Exported {len(df)} movies → CSV, Excel, JSON")


# ── Main scrape function ──────────────────────────────────────────────────────
def scrape():
    """Full scrape pipeline. Returns cleaned DataFrame."""
    driver = get_driver()

    if not load_page(driver):
        driver.quit()
        raise RuntimeError("Failed to load IMDb page after retries.")

    rows   = driver.find_elements(By.CSS_SELECTOR, CSS_ROW)
    print(f"  Found {len(rows)} movie rows")

    movies = [parse_row(row, idx) for idx, row in enumerate(rows, start=1)]
    movies = [m for m in movies if m is not None]  # drop failed rows
    driver.quit()
    print(f"  Scraped {len(movies)} movies successfully")

    df = clean_dataframe(movies)
    export_data(df, movies)
    return df


# ── Allow direct run ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    scrape()