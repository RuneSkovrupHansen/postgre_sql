import psycopg2


def main():

    # TODO place config in .ini file
    conn = psycopg2.connect(
        host="localhost",
        database="dvdrental",
        user="postgres",
        password="1234"
    )

    # Cursor is an object that can interact with a db
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM actor")

    # Retrieve query results
    records = cursor.fetchall()

    print(records)


if __name__ == "__main__":
    main()
