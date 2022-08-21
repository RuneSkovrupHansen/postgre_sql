from sqlalchemy.orm import Session, registry, declarative_base, relationship
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, ForeignKey, insert, select

"""The Core module of SQLAlchemy interacts with the database using normal queries. The ORM module uses the Core module to interact with the database through objects."""


def main():
    engine = create_engine("sqlite+pysqlite:///:memory:",
                           echo=True, future=True)

    # --- Core & ORM ---

    # Core w. text

    # sqlite - The kind of database, links alchemy to an object known as a dialect.
    # pysqlite - What DBAPI are we using. Third party driver for interaction with particular db. If omitted alchemy will use default DBAPI.
    # /:memory - In-memory db only. Perfect for experimenting, does not require server or file creation.

    with engine.connect() as conn:
        result = conn.execute(text("select 'hello world'"))
        print(result.all())

    # Using core, Connection object is how all interaction with a db is done.
    # Connection object is an open resource against database, scope should always be limited.

    # Changes are not committed by default.

    # "commit as you go"
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE some_table (x int, y int)"))
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
        )
        conn.commit()

    # Note that several parameters are passed as a list for the INSERT statement.

    # "begin once"
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 6, "y": 8}, {"x": 9, "y": 10}]
        )

    # Changes are automatically committed or rolled back in case of an exception.

    with engine.connect() as conn:
        result = conn.execute(text("SELECT x, y FROM some_table"))
        for row in result:
            print(f"x: {row.x}  y: {row.y}")

    # Parameter specified using ':<name>' syntax in text(), the value is passed as the second argument.
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT x, y FROM some_table WHERE y > :y"),
            {"y": 2}
        )
        for row in result:
            print(f"x: {row.x}  y: {row.y}")

    # Bundling parameters with the statement. Common way.
    stmt = text(
        "SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y").bindparams(y=6)
    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            print(f"x: {row.x}  y: {row.y}")

    # ORM

    # Working with ORM the primary interactive object is Session. Similar to Connection, and it uses it underneath. If non-ORM constructs are passed to to the Session it will simply pass them on to the connection.

    # commit as you go" behavior.

    stmt = text(
        "SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y").bindparams(y=6)
    with Session(engine) as session:
        result = session.execute(stmt)
        for row in result:
            print(f"x: {row.x}  y: {row.y}")

    # Passing parameters to make several executions. It is called twice to run with both sets of parameters.

    with Session(engine) as session:
        result = session.execute(
            text("UPDATE some_table SET y=:y WHERE x=:x"),
            [{"x": 9, "y": 11}, {"x": 13, "y": 15}]
        )
        session.commit()

    # --- MetaData ---

    # database metadata - Python objects that represent database concepts like tables and columns. Allows for fluent composable construction of SQL queries.
    # Used both Core and ORM styles.

    # Table object represent a database table. Can be declared in core or reflected from existing db.

    metadata_obj = MetaData()

    # Common to a single meta data object for all tables. All tables with relations should be placed in the same object.

    # Core

    # Initialization of a table for users. Assigns itself to the meta data object. Types represent SQL datatypes.

    user_table = Table(
        "user_account",  # Name of the table
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("name", String(30)),
        Column("fullname", String),
    )

    # Print table columns
    print(user_table.c.keys())

    # user_table.primary_key is an object representing the primary key. Said to be declared implicitly. Foreign keys are declared explicitly.

    address_table = Table(
        "address",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("user_id", ForeignKey("user_account.id"), nullable=False),
        Column("email_address", String, nullable=False)
    )

    metadata_obj.create_all(engine)

    # ORM

    # Create the same tables using ORM style.

    mapper_registry = registry()

    # Automatically includes metadata object.

    # Declare Table objects indirectly by descending from a common base class.
    Base = mapper_registry.generate_base()

    # Base = declarative_base(), can also be used to generate registry and base.

    class User(Base):
        __tablename__ = "user_account"

        id = Column(Integer, primary_key=True)
        name = Column(String(30))
        fullname = Column(String)
        addresses = relationship("Address", back_populates="user")

        # !r calls the repr of the supplied value
        def __repr__(self):
            return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r}"

    class Address(Base):
        __tablename__ = 'address'

        # The name of the attribute is the column name
        id = Column(Integer, primary_key=True)
        email_address = Column(String, nullable=False)
        user_id = Column(Integer, ForeignKey('user_account.id'))
        user = relationship("User", back_populates="addresses")

        def __repr__(self):
            return f"Address(id={self.id!r}, email_address={self.email_address!r})"

    # Inheriting from Base automatically provides the classes with a Table. User.__table__

    # Methods automatically get an __init__ to create an object from the table.

    # DDL = data definition language

    # For both Core and ORM the DDL, is said to be emitted to the database when the data, that is, tables, etc. is committed to the db.

    # emit CREATE statements given ORM registry
    mapper_registry.metadata.create_all(engine)

    # Base.metadata.create_all(engine) will do the same.

    # Table Reflection

    some_table = Table("some_table", metadata_obj, autoload_with=engine)

    print(some_table)

    # --- Inserting data ---

    # Core

    stmt = insert(user_table).values(
        name='spongebob', fullname="Spongebob Squarepants")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()

    # Another way to commit changes, multiple changes. Automatically uses executemany
    with engine.connect() as conn:
        result = conn.execute(
            insert(user_table),
            [
                {"name": "sandy", "fullname": "Sandy Cheeks"},
                {"name": "patrick", "fullname": "Patrick Star"}
            ]
        )
        conn.commit()

    # returning statement return last index that was inserted. In this case also the default values.
    insert_stmt = insert(address_table).returning(
        address_table.c.id, address_table.c.email_address)

    # --- Selecting data ---

    # Core

    # Use of select() statement, which can be passed to connection or session.
    stmt = select(user_table).where(user_table.c.name == 'spongebob')
    print(stmt)

    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(row)

    # ORM

    # Using the ORM approach indicates that the return should also be ORM, which is not true for the Core approach.
    stmt = select(User).where(User.name == 'spongebob')
    with Session(engine) as session:
        for row in session.execute(stmt):
            print(row)

    # Selecting columns.
    # select can be used, for simple cases this resolved to FROM clause in SQL statement.

    # Core

    print(select(user_table))
    print(select(user_table.c.name, user_table.c.fullname))

    # ORM

    print(select(User))
    row = session.execute(select(User)).first()
    row[0]  # The user

    # session.scalars() can be used to get the user directly.
    user = session.scalars(select(User)).first()
    user  # The user

    # Selecting specific columns
    print(select(User.name, User.fullname))

    # .label() can be used to label colum retrieved with select.

    # WHERE clause, use of standard Python operators.

    # Produces a single WHERE clause.
    print(select(user_table).where(user_table.c.name == 'squidward'))

    # Produces multiple where clauses.
    print(
        select(address_table.c.email_address).
        where(user_table.c.name == 'squidward').
        where(address_table.c.user_id == user_table.c.id)
    )

    # Also possible to pass multiple arguments to the where clause

    # AND and OR clauses exist. See source.
    # https://docs.sqlalchemy.org/en/14/tutorial/data_select.html#selecting-rows-with-core-or-orm

    # FROM and JOINs

    # From a single table, single FROM argument.
    print(select(user_table.c.name))

    # From two tables, two FROM, i.e. FROM table_a, table_b
    print(select(user_table.c.name, address_table.c.email_address))

    # JOIN specified, from table_a joined on table_b
    print(
        select(user_table.c.name, address_table.c.email_address).
        join_from(user_table, address_table)
    )

    # The ON clause is inferred. If tables have a ForeignKeyConstraint between them.
    # Also possible to manually specify the ON clauses.

    # OUTER and FULL joins can be specified.

    # Up next!
    # https://docs.sqlalchemy.org/en/14/tutorial/data_select.html#order-by-group-by-having


if __name__ == "__main__":
    main()
