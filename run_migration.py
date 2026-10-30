import psycopg2

DATABASE_URL = "postgresql://myduka_db_ibnn_user:NJ7RvLB3ZeufKlBNEmXKeQiLSyT1IYS@dpg-dadvut10dsc738a9seg-a/myduka_db_ibnn"

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Replace with your actual ALTER TABLE query
cur.execute("ALTER TABLE your_table_name ADD COLUMN your_column_name VARCHAR(255);")

conn.commit()
cur.close()
conn.close()
print("Migration executed successfully!")