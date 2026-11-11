
from utils.db_connect import get_db_connection


def test_get_db_connection():

    connection = None

    try:
        connection = get_db_connection()

        if connection:
            print("Database connection established successfully.")

            cursor = connection.cursor()
            cursor.execute("SELECT current_database();")

            result = cursor.fetchone()

            print("Connected Database:", result[0])

            cursor.close()

    except Exception as e:
        print("Database connection failed:", e)

    finally:
        if connection:
            connection.close()
            print("Database connection closed.")


if __name__ == "__main__":
    test_get_db_connection()
