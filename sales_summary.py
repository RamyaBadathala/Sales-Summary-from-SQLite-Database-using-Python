import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Create and connect to the SQLite database
db_file = "sales_data.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Step 2: Create the sales table (only if it doesn't exist)
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
);
""")

# Optional: Insert sample data if table is empty
cursor.execute("SELECT COUNT(*) FROM sales")
if cursor.fetchone()[0] == 0:
    sample_data = [
        ("Apples", 10, 0.5),
        ("Oranges", 20, 0.6),
        ("Bananas", 15, 0.3),
        ("Apples", 5, 0.5),
        ("Oranges", 10, 0.6),
        ("Bananas", 25, 0.3),
    ]
    cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sample_data)
    conn.commit()

# Step 3: Run SQL query to get sales summary
query = """
SELECT product, 
       SUM(quantity) AS total_qty, 
       ROUND(SUM(quantity * price), 2) AS revenue
FROM sales
GROUP BY product
"""
df = pd.read_sql_query(query, conn)

# Step 4: Display the results
print("Sales Summary:")
print(df)

# Step 5: Plot bar chart of revenue by product
df.plot(kind='bar', x='product', y='revenue', legend=False, color='skyblue')
plt.title("Revenue by Product")
plt.ylabel("Revenue ($)")
plt.xlabel("Product")
plt.tight_layout()
plt.savefig("sales_chart.png")
plt.show()

# Step 6: Close connection
conn.close()

