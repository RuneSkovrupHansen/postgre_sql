import psycopg2

# Start / stop postgresql
# sudo service postgresql start / stop


def connect_to_db(database, host="localhost", user="postgres", password="1234"):
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
    except psycopg2.OperationalError as e:
        print(f"Unable to connect to db, error: {e}")
        return None

    return conn.cursor()


def main():

    cur = connect_to_db("dvdrental")
    if cur is None:
        return

    query = "SELECT * FROM actor WHERE first_name = 'Bob'"

    cur.execute(query)
    records = cur.fetchall()

    print(records)


if __name__ == "__main__":
    main()
