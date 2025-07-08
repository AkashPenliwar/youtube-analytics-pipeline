import psycopg2

def connect_to_postgres():
    try:
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            database="youtube_analytics",
            user="postgres",
            password="Akash1812"  # Replace with your actual PostgreSQL password
        )

        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(" Connected to PostgreSQL:", version)

        cursor.close()
        connection.close()

    except Exception as error:
        print(" Could not connect:", error)

if __name__ == "__main__":
    connect_to_postgres()
