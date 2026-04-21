"""
IMDb Top 250 Scraper & Analyzer
================================
Entry point — imports and calls functions from Scrape and Analysis modules.

Usage:
    python Main.py

Pipeline:
    Step 1 → Scrape.scrape()   : Headless Selenium scraper for JS-rendered IMDb
    Step 2 → Analysis.analyze(): Matplotlib charts + console stats
"""

import Scrape
import Analysis


def run_pipeline():
    # ── Step 1: Scrape ────────────────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("  Step 1 — Scraping IMDb Top 250")
    print("=" * 55)
    df = Scrape.scrape()

    # ── Step 2: Analyze ───────────────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("  Step 2 — Analysis & Chart Generation")
    print("=" * 55)
    Analysis.analyze()

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("  Pipeline complete.")
    print(f"  Movies scraped : {len(df)}")
    print("  Data files     : imdb_top250.csv / .xlsx / .json")
    print("=" * 55)


if __name__ == "__main__":
    run_pipeline()