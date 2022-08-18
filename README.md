Repository for playing around with PostgreSQL

# postgresql service

sudo service postgresql status
sudo service postgresql start
sudo service postgresql stop

Open psql as default user postgres:

    sudo -u postgres psql

psql – a terminal-based front-end to PostgreSQL database server

It is possible to specify server host or socket directory and port of the server, while calling psql to connect to a database.


# Connection

By default, connection to a local server is established through a socket. This seems to have several side effects.

Note that in the commands above, we're actually using sudo to specify that the user should be set to 'postgres' before the psql command is run. This ensures that we log in as postgres.

    sudo -u postgres psql

Before making queries we must connect to a specific database.

## Authentication

Different methods of authentication can be specified for the types of connection. For Unix domain socket the default is "peer" which pulls the username from the system.

Authentication:
https://stackoverflow.com/a/18664239/13308972

Changing password:
https://stackoverflow.com/questions/12720967/how-to-change-postgresql-user-password

By changing changing peer to postgres, it's possible to connect using the command:

psql -U postgres -W

This command explicitly sets the user to "postgres" and forces a password prompt. Since the user info is no longer pulled by the system, this command works.

Another option is md5 which is more secure.


Documentation:

Client authentication is controlled by a configuration file, which traditionally is named pg_hba.conf and is stored in the database cluster's data directory. (HBA stands for host-based authentication.) A default pg_hba.conf file is installed when the data directory is initialized by initdb. 

# Load / restore database

sudo -u postgres pg_restore -d <database> <file>

    The file must be a .tar file.


# Commands

It's possible to use both psql commands and SQL commands to control psql. It would seem that postgresql stores it's information in a postgres db as well, which is what is making this possible.

Command:

* \c <name> - connect to db
* DROP DATABASE <name> - drop db

Before using commands to query a database, you must first connect to it. Example:
`\c <database>`

# Querying data

## SELECT

Select all columns from table customer:
`SELECT * FROM customers;`

Select specific columns from table customer:
`SELECT first_name, last_name FROM customers;`


## CONCATENATION

Use of concatenate operator:
`SELECT first_name || " " || last_name, email FROM customers;`

Note the call above will results in two columns, <first_name> <last_name> and <email>. The names are concatenated into a single column. These columns can be assigned a meaningful alias.

Column aliases are assigned using the `AS` operator. Example:
`SELECT first_name || ' ' || last_name AS full_name, email FROM customer;`

AS can also be omitted. Use quotation marks to mark a string with spaces.


## ORDER BY
Returned vales can be sorted using the `ORDER BY` operator. The operator takes one or more sort expressions. Separated by comma. ASC / DESC can be specified, ASC is the default.

PostgreSQL evaluates FROM -> SELECT -> ORDER BY, meaning that any aliases specified in the SELECT clause must be used in the ORDER BY clause.

Example:
`SELECT first_name, last_name, email FROM customer ORDER BY last_name;`
`SELECT first_name, last_name, email FROM customer ORDER BY last_name DESC;`

Multiple expressions can specified. Separated by comma. They are ordered by the order of the expressions:
`SELECT first_name, last_name, email FROM customer ORDER BY last_name DESC;`
`SELECT first_name, last_name, email FROM customer ORDER BY last_name, first_name ASC;`

Possible to use functions while writing queries. Example of LENGTH() function:
`SELECT first_name, last_name, LENGTH(last_name) last_name_length FROM customer ORDER BY last_name_length, first_name;`

`NULL` is a marker that indicates mission or unknown data. Working on data with NULL values we can ordered by ORDER BY clause. Syntax:
`ORDER BY sort_expresssion [ASC | DESC] [NULLS FIRST | NULLS LAST]`


## DISTINCT, DISTINCT ON()

`DISTINCT` can be used in SELECT to remove duplicate rows from a set.
`SELECT DISTINCT first_name FROM actor ORDER BY first_name;`

If multiple columns are specified, the evaluation is based on the combination of these values.
`SELECT DISTINCT first_name, last_name FROM actor ORDER BY first_name;`

`SELECT DISTINCT ON(column) ...`
Can be used to select multiple columns but only filter based on a single column.
Supposedly a powerful function to skip some steps when extracting info.

Examples:

`SELECT DISTINCT color1, color2 FROM distinct_demo ORDER BY color1 NULLS LAST;`
Distinct on both columns.

`SELECT DISTINCT ON(color1) color1, color2 FROM distinct_demo ORDER BY color1 NULLS LAST;`
Only distinct on color1, but still retrieving both columns color1 and color2.

# Filtering data

## WHERE

https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-where/

WHERE filters rows returned from select statement. Example:
`SELECT select_list FROM table_name WHERE condition ORDER BY sort_expression;`

Filters based condition. Condition must be boolean expression or a combination of boolean expressions.

Order of evaluation for Postgres: FROM -> WHERE -> SELECT -> ORDER BY

Condition can be formed from comparison and logical operators. See source.

Example, creating new column with full name for all customers with first name bob.
`SELECT first_name || ' ' || last_name AS full_name FROM customer WHERE first_name = 'Bob';`

Example, multiple conditions.
`SELECT first_name, last_name FROM customer WHERE first_name = 'Jamie' AND last_name = 'Rice';`

Use of a list to check multiple values in column:
`SELECT first_name, last_name FROM customer WHERE first_name IN ('Jamie', 'Tyrone');`

Wildcard and LENGTH:
`SELECT first_name, LENGTH(first_name) as name_length FROM customer WHERE first_name LIKE 'R%' and LENGTH(first_name) BETWEEN 3 AND 5 ORDER BY name_length;`

Wildcard operator % will match anything with the wildcard.

Many different options. Can accept on a first_name wildcard and then negate on a specific last_name.


## LIMIT

The LIMIT clause can be used to limit the number of returned rows generated by the query.

Example:
`SELECT film_id, title FROM film ORDER BY film_id LIMIT 10;`

OFFSET can be used to offset the limit:
`SELECT film_id, title FROM film ORDER BY film_id LIMIT 10 OFFSET 5;`

Typically used to get the X most of some column, for example, the most expensive items can be retrieved by sorting by value and limiting return to 10.


## FETCH

LIMIT is not a SQL-standard. To conform with standard SQL FETCH can be used.

Syntax:

OFFSET start { ROW | ROWS }
FETCH { FIRST | NEXT } [ row_count ] { ROW | ROWS } ONLY

Example:
`SELECT film_id, title FROM film ORDER BY title OFFSET 5 ROWS FETCH FIRST 10 ROW ONLY;`


## IN

IN operator is used in WHERE clause to check if a value matches any value in a list of values.

Syntax:
`value IN (value1,value2,...)`

List can also be a query:
`value IN (SELECT column_name FROM table_name);`

Is commonly used in place of multiple equality statements in a WHERE claus, or for more advanced statements which include the WHERE clause.

Can be negated using NOT, syntax:
`value NOT IN (value1,value2,...)`

It's possible to nest an entire query inside of the IF operator. This is called a subquery.

## BETWEEN

Operator to select between a range. Syntax:
`value BETWEEN low AND high;`

Equivalent to:
`value >= low and value <= high`

Can be negated with NOT.

Common to use in where claus.

Can also be used to check dates.


## LIKE

LIKE is an operator used in the WHERE clause to filter data. Used to match values with patterns.

Example of a pattern:
`Jen%`

Will match with anything that starts with Jen.

Can be negated with NOT.

`%` is a wildcard operator, will match with anything.

Also possible to use `_` which can serve as a wildcard for a single character.

Examples:
`'foo' LIKE 'foo', -- true`
`'foo' LIKE 'f%', -- true`
`'foo' LIKE '_o_', -- true`
`'bar' LIKE 'b_'; -- false`

Multiple wildcards can be combined to form quite advanced filtering options. Example:
`WHERE first_name LIKE '_her%'`

Example:
`SELECT customer_id, first_name, last_name FROM customer WHERE last_name LIKE '_s%' ORDER BY customer_id;`

The operator ILIKE will match case-insensitive.

There are also sign characters for these operations, ex. ~~ = LIKE.


## IS NULL

Any comparison with NULL results in NULL. That is, any check against NULL with the equality operator "=" will result in null.

NULL = NULL, returns false.

NULL is NULL, returns true.

When checking against NULL or NOT NULL we must use IS NULL to get a meaningful answer.

Examples:
`'Hello' != NULL, false`
`'Hello' = NULL, false`
`'Hello' IS NULL, false`
`'Hello' IS NOT NULL, true`


# Joining multiple tables

Combining one or more tables based on the values of common columns between related tables. Common columns are the primary keys of the column of the first table and foreign key columns of the second table.

A primary key in a table is the unique key for a table. A foreign key is a primary key in another table.

See source for examples and diagrams of the joins.

Different types of join:

* Inner
* Left
* Right
* Full

Left right and full joins are also called outer. IS NULL can be used to get non-overlapping values.

## Table aliases

Temporarily assign new names during execution of a query.

Syntax:
`table_name AS alias_name;`

AS is optional, but a lot more readable.

It is common to qualify columns by using the table name with the following syntax:
`SELECT table_name.column_name;`

This is used to avoid naming conflicts if multiple tables have the same column names.

Alias can be used to shorten table names.

Example:

```
SELECT
	c.customer_id,
	first_name,
	amount,
	payment_date
FROM
	customer c
INNER JOIN payment p 
    ON p.customer_id = c.customer_id
ORDER BY 
   payment_date DESC;
```

Aliases must use aliases to self-join tables, example:

```
SELECT
    e.first_name employee,
    m .first_name manager
FROM
    employee e
INNER JOIN employee m 
    ON m.employee_id = e.manager_id
ORDER BY manager;
```

Table employee is referenced twice.


## INNER JOIN

In relational database data is often distributed in multiple tables to select complete data, you need to select from more tables.

INNER JOIN can be used to combine data.

Tables must be joined on column with common values. Most of the time it's an id or similar.

Inner join creates rows of all selected columns where the INNER JOIN ON was equal.

Common to name joined table with alias and reference it through the alias.

Example:

```
SELECT
    c.customer_id,
    first_name,
    last_name,
    amount,
    payment_date
FROM
    customer c
INNER JOIN payment 
    ON payment.customer_id = c.customer_id
ORDER BY c.customer_id;
```

Possible to combine with WHERE CLAUSE to filter rows.

Since the tables are joined on a column with the same name, the USING() clause can be used instead of the ON clause with equality. Example:

```
SELECT
	c.customer_id,
	first_name,
	last_name,
	email,
	amount,
	payment_date
FROM
	customer c
INNER JOIN payment p
    USING(customer_id)
WHERE
    c.customer_id = 2;
```

Example of joining multiple tables and importance of aliases:

```
SELECT
	c.customer_id,
	c.first_name customer_first_name,
	c.last_name customer_last_name,
	s.first_name staff_first_name,
	s.last_name staff_last_name,
	amount,
	payment_date
FROM
	customer c
INNER JOIN payment p 
    ON p.customer_id = c.customer_id
INNER JOIN staff s 
    ON p.staff_id = s.staff_id
ORDER BY payment_date;
```

## LEFT JOIN

Left refers to the first specified table. Takes all values from the left table, and fills in any value from the right table when the JOIN condition matches.

NULL is set as the value for rows which do not have a match in the right table.

Example, getting all titles where inventory is NULL:

```
SELECT
	f.film_id,
	title,
	inventory_id
FROM
	film f
LEFT JOIN inventory i
   ON i.film_id = f.film_id
WHERE i.film_id IS NULL
ORDER BY title;
```

Note that the NULL values of LEFT JOIN non matches from the right table is used in the WHERE clause.

USING() syntax can be used for columns with the same name.

## RIGHT JOIN

Left refers to the table mentioned in the FROM clause, and right refers to the table mentioned in the JOIN clause.

RIGHT join takes all values from the right table, and fills in NULL for any missing values on the left table.

In other words, the RIGHT JOIN selects all rows from the right table whether or not they have matching rows from the left table.

Example:
https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-right-join/

## Self-join

Join a table with itself. Typically used to query hierarchical data or to compare rows within the same table.

Must specify same table twice using different table aliases, syntax:

```
SELECT select_list
FROM table_name t1
INNER JOIN table_name t2 ON join_predicate;
```

Left and right joins can also be used.

https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-self-join/

Hierarchical example, employee / manager example.

```
SELECT
    e.first_name || ' ' || e.last_name employee,
    m .first_name || ' ' || m .last_name manager
FROM
    employee e
LEFT JOIN employee m ON m .employee_id = e.manager_id
ORDER BY manager;
```

Compare data from the same row, film length example.

```
SELECT
    f1.title,
    f2.title,
    f1.length
FROM
    film f1
INNER JOIN film f2 
    ON f1.film_id <> f2.film_id AND 
       f1.length = f2.length;
```

Notice the use of multiple ON conditions

## FULL JOIN

Syntax:

```
SELECT * FROM A
FULL [OUTER] JOIN B on A.id = B.id;
```

The result includes the matching rows from both tables, and also the rows that do not match.

Can be nice to check where certain table have NULL values.


## CROSS JOIN

If T1 has n rows and T2 has m rows, the result set will have nxm rows. For example, the T1 has 1,000 rows and T2 has 1,000 rows, the result set will have 1,000 x 1,000 = 1,000,000 rows.

Creates a list of all possible combinations.

Syntax:

```
SELECT select_list
FROM T1
CROSS JOIN T2;
```

## NATURAL JOIN

A natural join is a join that creates an implicit join based on the same column names in the joined tables.

Syntax:

```
SELECT select_list
FROM T1
NATURAL [INNER, LEFT, RIGHT] JOIN T2;
```

The convenience of the NATURAL JOIN is that it does not require you to specify the join clause because it uses an implicit join clause based on the common column.


# Grouping data

## GROUP BY