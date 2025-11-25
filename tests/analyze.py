import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def compare_followers_vs_views(db_path):
    conn = sqlite3.connect(db_path)

    query = """
    SELECT Titles.id, Titles.title, Titles.views, SUM(Actors.number_followers) AS actors_popularity
    FROM Roles
    JOIN Actors ON Roles.actor_id = Actors.id
    JOIN Titles ON Roles.title_id = Titles.id
    WHERE Actors.number_followers IS NOT NULL AND Titles.views IS NOT NULL
    GROUP BY Titles.id, Titles.title;
    """

    try:
        df = pd.read_sql_query(query, conn)
        print("Processing query...")

        conn.close()

    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
        exit(1)

    # Compute correlation coefficient
    correlation = df['actors_popularity'].corr(df['views'])
    print(f"Correlation coefficient: {correlation:.4f}")

    # Standardize the data
    # x_bins = [      # Follower count standardization
    #     0,
    #     1_000,
    #     10_000,
    #     20_000,
    #     50_000,
    #     100_000,
    #     250_000,
    #     float('inf')
    # ]
    #
    # x_labels = [
    #     "< 1k",
    #     "1-10k",
    #     "10-20k",
    #     "20-50k",
    #     "50-100k",
    #     "100-250k",
    #     "+ 250k"
    # ]
    # df['x_bin'] = pd.cut(df['actors_popularity'], bins=x_bins, labels=x_labels, include_lowest=True)
    #
    # y_bins = [        # View count standardization
    #     0,
    #     1_000_000,
    #     10_000_000,
    #     50_000_000,
    #     100_000_000,
    #     200_000_000,
    #     500_000_000,
    #     float('inf')
    # ]
    #
    # y_labels = [
    #     "< 1M",
    #     "1-10M",
    #     "10-50M",
    #     "50-100M",
    #     "100-200M",
    #     "200-500M",
    #     "+ 500M"
    # ]
    #
    # df['y_bin'] = pd.cut(df['views'], bins=y_bins, labels=y_labels, include_lowest=True)

## Log-Log Scatter Plot + Regression Line
    plt.figure(figsize=(10, 6))

    # Scatter on log-log scale
    plt.scatter(df['actors_popularity'], df['views'], alpha=0.6, label="Shows")

    # Regression line (in log space)
    x = df['actors_popularity']
    y = df['views']

    log_x = np.log10(x)
    log_y = np.log10(y)

    m, b = np.polyfit(log_x, log_y, 1)  # regression in log space

    x_sorted = np.sort(x)
    y_pred = 10 ** (m * np.log10(x_sorted) + b)

    plt.plot(x_sorted, y_pred, color='red', linewidth=2, label="Regression line")

    plt.xscale('log')
    plt.yscale('log')

    plt.xlabel("Cast popularity (log scale)")
    plt.ylabel("Show popularity (log scale)")
    plt.title("Cast Popularity vs Show Popularity (Log-Log, with Regression)")
    plt.grid(True, which="both", linestyle='--', alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ---------------------------------------------------------
    # 2. HEATMAP (2D density using hist2d)
    # ---------------------------------------------------------

    plt.figure(figsize=(10, 6))
    plt.hist2d(df['actors_popularity'], df['views'], bins=25, cmap='Blues')
    plt.colorbar(label='Density')

    plt.xscale('log')
    plt.yscale('log')

    plt.xlabel("Cast popularity (log scale)")
    plt.ylabel("Show popularity (log scale)")
    plt.title("Density Heatmap: Cast Popularity vs Show Popularity")
    plt.tight_layout()
    plt.show()

    # ---------------------------------------------------------
    # 3. Save original scatterplot (optional)
    # ---------------------------------------------------------

    output_folder = os.path.join("..", "results")
    os.makedirs(output_folder, exist_ok=True)
    filepath = os.path.join(output_folder, "scatterplot.png")

    plt.figure(figsize=(10, 6))
    plt.scatter(df['actors_popularity'], df['views'])
    plt.xlabel("Cast popularity")
    plt.ylabel("Show popularity")
    plt.title("Original Scatterplot (Linear Scale)")
    plt.grid(True)
    plt.savefig(filepath)
    print(f"Original scatterplot saved to: {filepath}")
    plt.close()

    # Save the file
    output_folder = os.path.join("..", "results")  # Saves the results under the data folder
    os.makedirs(output_folder, exist_ok=True)
    filename = "scatterplot.png"
    filepath = os.path.join(output_folder, filename)


    # Plot results
    plt.scatter(df['actors_popularity'], df['views'])
    plt.xlabel("Cast popularity")
    plt.ylabel("Show popularity")
    plt.title("Relationship between cast popularity and show popularity")
    plt.grid(True)
    plt.savefig(filepath)  # Save the image to file
    print(f"Scatterplot saved to {filepath} as {filename}")
    plt.show(block=False)
    plt.pause(2)

    input("Press Enter to close...")
    plt.close()


db_path = '../db/verticals_database.db'
compare_followers_vs_views(db_path)