import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Connect to the existing SQLite database
conn = sqlite3.connect("sales_data.db")

# Step 2: Define and run the SQL query
query = """
SELECT product, 
       SUM(quantity) AS total_qty, 
       ROUND(SUM(quantity * price), 2) AS revenue
FROM sales
GROUP BY product
"""
df = pd.read_sql_query(query, conn)

# Step 3: Display the result
print("Sales Summary:")
print(df)

# Step 4: Plot the revenue by product
df.plot(kind='bar', x='product', y='revenue', legend=False, color='orange')
plt.title("Revenue by Product")
plt.ylabel("Revenue ($)")
plt.xlabel("Product")
plt.tight_layout()
plt.savefig("sales_chart.png")
plt.show()

# Step 5: Close the database connection
conn.close()
