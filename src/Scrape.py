import pandas as pd
import matplotlib.pyplot as plt
import os


# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_DIR    = os.path.join(BASE_DIR, '..', 'data')
CHARTS_DIR  = os.path.join(BASE_DIR, '..', 'charts')


# ── Loader ────────────────────────────────────────────────────────────────────
def load_data(path=None):
    """Load and type-cast the scraped CSV."""
    if path is None:
        path = os.path.join(DATA_DIR, 'imdb_top250.csv')
    df = pd.read_csv(path)
    df['year']        = df['year'].astype('Int64')
    df['imdb_rating'] = pd.to_numeric(df['imdb_rating'], errors='coerce')
    return df


# ── Individual chart functions ────────────────────────────────────────────────
def plot_rating_distribution(df):
    """Histogram of IMDb rating spread across all 250 movies."""
    plt.figure(figsize=(10, 6))
    plt.hist(df['imdb_rating'].dropna(), bins=20, edgecolor='black', color='steelblue')
    plt.title('Distribution of IMDb Ratings — Top 250 Movies')
    plt.xlabel('IMDb Rating')
    plt.ylabel('Number of Movies')
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, 'rating_distribution.png'), dpi=150)
    plt.close()
    print("  Saved: charts/rating_distribution.png")


def plot_top10(df):
    """Horizontal bar chart of top 10 movies by rating."""
    top = df.sort_values('imdb_rating', ascending=False).head(10)
    plt.figure(figsize=(12, 7))
    bars = plt.barh(top['title'], top['imdb_rating'], color='steelblue')
    plt.xlabel('IMDb Rating')
    plt.title('Top 10 Movies by IMDb Rating')
    plt.gca().invert_yaxis()
    for bar, val in zip(bars, top['imdb_rating']):
        plt.text(
            bar.get_width() - 0.05,
            bar.get_y() + bar.get_height() / 2,
            f'{val}', va='center', ha='right',
            color='white', fontweight='bold'
        )
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, 'top_10_movies.png'), dpi=150)
    plt.close()
    print("  Saved: charts/top_10_movies.png")


def plot_rating_vs_year(df):
    """Scatter plot — does release year correlate with rating?"""
    plt.figure(figsize=(10, 6))
    plt.scatter(
        df['year'], df['imdb_rating'],
        alpha=0.6, color='steelblue',
        edgecolors='white', linewidth=0.5
    )
    plt.title('IMDb Rating vs Release Year')
    plt.xlabel('Year')
    plt.ylabel('IMDb Rating')
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, 'rating_vs_year.png'), dpi=150)
    plt.close()
    print("  Saved: charts/rating_vs_year.png")


def plot_avg_rating_by_decade(df):
    """Line chart — average rating grouped by decade."""
    df = df.copy()
    df['decade']  = (df['year'] // 10) * 10
    decade_avg    = df.groupby('decade')['imdb_rating'].mean().reset_index()
    plt.figure(figsize=(10, 6))
    plt.plot(
        decade_avg['decade'], decade_avg['imdb_rating'],
        marker='o', color='steelblue', linewidth=2
    )
    plt.fill_between(decade_avg['decade'], decade_avg['imdb_rating'],
                     alpha=0.1, color='steelblue')
    plt.title('Average IMDb Rating by Decade')
    plt.xlabel('Decade')
    plt.ylabel('Average IMDb Rating')
    plt.xticks(
        decade_avg['decade'],
        [f"{int(d)}s" for d in decade_avg['decade']],
        rotation=45
    )
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, 'avg_rating_by_decade.png'), dpi=150)
    plt.close()
    print("  Saved: charts/avg_rating_by_decade.png")


# ── Stats printer ─────────────────────────────────────────────────────────────
def print_stats(df):
    """Print basic dataset statistics to console."""
    print("  Basic Statistics:")
    print(df.describe().to_string())
    print(f"\n  Total movies  : {len(df)}")
    print(f"  Rating range  : {df['imdb_rating'].min()} – {df['imdb_rating'].max()}")
    print(f"  Year range    : {df['year'].min()} – {df['year'].max()}")


# ── Main analysis function ────────────────────────────────────────────────────
def analyze(path=None):
    """Run all analysis steps on the scraped CSV."""
    os.makedirs(CHARTS_DIR, exist_ok=True)
    df = load_data(path)
    print_stats(df)
    plot_rating_distribution(df)
    plot_top10(df)
    plot_rating_vs_year(df)
    plot_avg_rating_by_decade(df)
    print("\n  All charts saved successfully.")


# ── Allow direct run ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    analyze()