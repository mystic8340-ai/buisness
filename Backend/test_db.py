
from database import get_connection

connection = None

try:
    connection = get_connection()

    print("SUCCESS: Connected to MySQL!")

    cursor = connection.cursor()
    cursor.execute("SELECT DATABASE(), @@port")
    result = cursor.fetchone()

    print("Database:", result[0])
    print("Port:", result[1])

    cursor.close()

except Exception as error:
    print("CONNECTION FAILED")
    print(error)

finally:
    if connection is not None and connection.is_connected():
        connection.close()
        print("Connection closed.")
