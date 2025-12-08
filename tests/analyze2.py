import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

def analyze_actor_hit_rates(db_path: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)

    query = """
    SELECT
        a.id AS actor_id,
        a.name AS actor_name,
        COUNT(*) AS total_titles,
        SUM(CASE WHEN t.views > 50000000 THEN 1 ELSE 0 END) AS total_hits,
        ROUND(
            1.0 * SUM(CASE WHEN t.views > 50000000 THEN 1 ELSE 0 END) 
            / COUNT(*), 
            3
        ) AS hit_rate,
        ROUND(AVG(t.views), 0) AS avg_views,
        MAX(t.views) AS max_views
    FROM Roles r
    JOIN Titles t ON r.title_id = t.id
    JOIN Actors a ON a.id = r.actor_id
    GROUP BY a.id
    ORDER BY hit_rate DESC;
    """

    df = pd.read_sql_query(query, conn)
    df = df.dropna() # Clean data ignore Null values

    conn.close()
    return df

# Plot actors hit rates as bar graph
def plot_all_hit_rates(df):
    # Sort so top hit_rate is first
    df_sorted = df.sort_values(by="hit_rate", ascending=False)

    # Get only the top 10 actors
    top10 = df_sorted.head(15)

    plt.figure(figsize=(12, 6))
    plt.bar(top10["actor_name"], top10["hit_rate"], color='skyblue')

    plt.title("Top Actors By Hit Rates (>50M View Titles)", fontsize=14)
    plt.xlabel("Actor Name", fontsize=12)
    plt.ylabel("Hit Rate", fontsize=12)
    plt.xticks(rotation=45, ha="right")

    plt.ylim(0, 1)   # hit rate is between 0 and 1
    plt.tight_layout()
    plt.show()

db_path = '../db/verticals_database.db'

df_hits = analyze_actor_hit_rates(db_path)
average_hit_rate = sum(df_hits["hit_rate"])/len(df_hits)
print(average_hit_rate)
plot_all_hit_rates(df_hits)

# plot_top_10_hit_rate(df_hits)
