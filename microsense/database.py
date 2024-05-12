import sqlite3
from typing import List
con = sqlite3.connect("./shared-volume/metrics.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS  metrics (timestamp INT, value REAL, metric VARCHAR(255))")

def insert_metric(timestamp, value, metric):
    cur.execute("INSERT INTO metrics (timestamp, value, metric) VALUES (?, ?, ?)", (timestamp, value, metric))
    con.commit()

def get_metrics(metric:str) -> List:
    cur.execute("SELECT * FROM metrics WHERE metric = ?", (metric,))
    return cur.fetchall()