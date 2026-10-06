import psycopg

connection = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="shopsphere",
    user="postgres",
    password="Postgres5432"
)

print("Database connection successful!")

connection.close()