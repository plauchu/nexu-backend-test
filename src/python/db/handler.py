import psycopg2
import json

conn = psycopg2.connect(host="localhost", user="postgres", password="1234", dbname="nexu", port=5432)
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS MODELS (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                average_price INT NOT NULL,
                brand_name TEXT NOT NULL
            );""")

cur.execute("""CREATE TABLE IF NOT EXISTS BRANDS (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                average_price INT
            );""")

with open('models.json', 'r') as file:
    db_backfill = json.load(file)

for data in db_backfill:
    cur.execute("INSERT INTO MODELS (name, average_price, brand_name) VALUES (%s, %s, %s)", (data["name"], data["average_price"], data["brand_name"]))

cur.execute("""INSERT INTO BRANDS (name, average_price)
               SELECT DISTINCT brand_name, ROUND(AVG(average_price), 0) AS average_price
               FROM MODELS
               GROUP BY brand_name
               ORDER BY brand_name ASC;""")

conn.commit()
cur.close()
conn.close()