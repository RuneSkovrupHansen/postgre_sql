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

GROUP BY clause divides ros returned from SELECT statement into groups. Aggregate function can be applied on sum of items. Ex. SUM(), COUNT().

Example query:
```
select c.customer_id, c.first_name || ' ' || c.last_name full_name, SUM(p.amount) total_amount FROM customer c INNER JOIN payment p USING(customer_id) GROUP BY c.customer_id ORDER BY total_amount DESC;
```

Note that to reference the output of an aggregator function, an alias must be used.

Can be grouped on multiple columns.

Example of DATE() to transform date column into comparable data.

## HAVING

The HAVING clause specifies a search condition for a group or an aggregate. The HAVING clause is often used with the GROUP BY clause to filter groups or aggregates based on a specified condition.

# Set operations

## Union

The UNION operator combines result sets of two or more SELECT statements into a single result set.

```
SELECT select_list_1
FROM table_expresssion_1
UNION
SELECT select_list_2
FROM table_expression_2
```

UNION_ALL to get full Venn diagram.

Duplicate entries removed with just UNION

## INTERSECT

The INTERSECT operator returns any rows that are available in both result sets.

```
SELECT select_list
FROM A
INTERSECT
SELECT select_list
FROM B;
```

## EXCEPT

Return the rows in the first query that does not appear in the output of the second query.

# Grouping sets, Cube and Rollup

## GROUPING SETS

The PostgreSQL GROUPING SETS clause can be used to generate multiple grouping sets in a query.

GROUP BY operator. SELECT aggregation operators like COUNT(), SUM(), etc, can be used to select from the group.

GROUPING SETS makes it possible to group by multiple things in a single query.

```
SELECT
    c1,
    c2,
    aggregate_function(c3)
FROM
    table_name
GROUP BY
    GROUPING SETS (
        (c1, c2),
        (c1),
        (c2),
        ()
);
```
## ROLLUP

SUBCLAUSE for GROUPING SETS to more quickly define sets to group by.

Ordering matters. See source.

```
SELECT
    c1,
    c2,
    c3,
    aggregate(c4)
FROM
    table_name
GROUP BY
    ROLLUP (c1, c2, c3);
```

Partials rolls possible

## CUBE

SUBCLAUSE for GROUPING SETS to get all possible combinations of groups from a list.

Ordering matters. See source.

Subcubes are possible.

```
SELECT
    c1,
    c2,
    c3,
    aggregate (c4)
FROM
    table_name
GROUP BY
    CUBE (c1, c2, c3);

```

# SUBQUERY

## SUBQUERY

Queries in queries. Allows us to construct complex statements.

Example, find movies with rental_rate higher than average. 1. query to find average, 2. query to find movies higher than average.

```
SELECT
	film_id,
	title,
	rental_rate
FROM
	film
WHERE
	rental_rate > (
		SELECT
			AVG (rental_rate)
		FROM
			film
	);
```

Query inside brackets is a subquery.

Order:

1. Subquery
2. Pass outer query
3. Execute outer query

Since subqueries can return zero or more rows, we can use IN to guard against zero cases.

```
SELECT
	film_id,
	title
FROM
	film
WHERE
	film_id IN (
		SELECT
			inventory.film_id
		FROM
			rental
		INNER JOIN inventory ON inventory.inventory_id = rental.inventory_id
		WHERE
			return_date BETWEEN '2005-05-29'
		AND '2005-05-30'
	);
```

EXISTS can wrap subquery and will return true or false depending on if any results is returned from subquery.

## ANY

The PostgreSQL ANY operator compares a value to a set of values returned by a subquery. 

`expresion operator ANY(subquery)`

ANY is equivalent to IN.

Essentially it's used to retrieve zero or more rows from an expression.

```
SELECT
    title,
    category_id
FROM
    film
INNER JOIN film_category
        USING(film_id)
WHERE
    category_id = ANY(
        SELECT
            category_id
        FROM
            category
        WHERE
            NAME = 'Action'
            OR NAME = 'Drama'
    );
```

Equivalent:

```
SELECT
    title,
    category_id
FROM
    film
INNER JOIN film_category
        USING(film_id)
WHERE
    category_id IN(
        SELECT
            category_id
        FROM
            category
        WHERE
            NAME = 'Action'
            OR NAME = 'Drama'
    );
```

## ALL

Similar use to ANY but instead all conditions must be fulfilled.

Use with numeric operators like < > >= <=, the value that is being compared is compared against ALL of the values.

For example in the query below, only film whose length is greater than all average lengths are selected.

```
SELECT
    film_id,
    title,
    length
FROM
    film
WHERE
    length > ALL (
            SELECT
                ROUND(AVG (length),2)
            FROM
                film
            GROUP BY
                rating
    )
ORDER BY
    length;
```

The length in the WHERE statement must be greater than ALL of the lengths returned from the other query.

## EXISTS

EXISTS() is a boolean operator that checks for the existence of rows in a subquery.

```
SELECT 
    column1
FROM 
    table_1
WHERE 
    EXISTS( SELECT 
                1 
            FROM 
                table_2 
            WHERE 
                column_2 = table_1.column_1);
```

Also filters the return in the process.

```
SELECT first_name,
       last_name
FROM customer c
WHERE EXISTS
    (SELECT 1
     FROM payment p
     WHERE p.customer_id = c.customer_id
       AND amount > 11 )
ORDER BY first_name,
         last_name;
```

Can be negated with NOT.

NULL exists and will return true.

# Common Table Expressions

## Common Table Expression -  CTE

Common table expressions, used to simplify complex queries.

```
WITH cte_name (column_list) AS (
    CTE_query_definition 
)
statement;
```

Example:

```
WITH cte_film AS (
    SELECT 
        film_id, 
        title,
        (CASE 
            WHEN length < 30 THEN 'Short'
            WHEN length < 90 THEN 'Medium'
            ELSE 'Long'
        END) length    
    FROM
        film
)
SELECT
    film_id,
    title,
    length
FROM 
    cte_film
WHERE
    length = 'Long'
ORDER BY 
    title; 
```

First part defines the name of the CTE, second part defines teh SELECT statement which populates the returned rows.

It's a way to split up a query to it is more manageable rather than having several nested subqueries.

Simplifies queries, easier to read.

WITH is the keyword for CTE's. For auxillary statements.

## Recursive query

Recursive query refers to a recursive CTE.

Syntax:

```
WITH RECURSIVE cte_name AS(
    CTE_query_definition -- non-recursive term
    UNION [ALL]
    CTE_query definion  -- recursive term
) SELECT * FROM cte_name;
```

See source.

# Modifying data

## INSERT

Insert a new row into a table with INSERT statement.

Syntax:

```
INSERT INTO table_name(column1, column2, …)
VALUES (value1, value2, …);
```

Return syntax:

`INSERT oid count`

Where oid is an internal PostgreSQL object identifier. Not important, commonly just 0.

Return column can be specified with RETURNING clause. Example:

```
INSERT INTO table_name(column1, column2, …)
VALUES (value1, value2, …)
RETURNING *;
```

AS clause can be used on the RETURNING clause.

When RETURNING clause is specified, the columns specified from the object is returned. Probably multiple rows when more values are specified.

Use of single quotes to insert character data.

All columns which are specified as NOT NULL must be passed when inserting into a row, they are required. Non-required columns assume default values when omitted, commonly NULL.

To insert data which requires single quote, use another single quote to escape it.

'YYYY-MM-DD' for columns with data type.

## INSERT MULTIPLE ROWS

Possible to insert multiple rows. Syntax:

```
INSERT INTO table_name (column_list)
VALUES
    (value_list_1),
    (value_list_2),
    ...
    (value_list_n);
```

```
INSERT INTO 
    links (url, name)
VALUES
    ('https://www.google.com','Google'),
    ('https://www.yahoo.com','Yahoo'),
    ('https://www.bing.com','Bing');
```

RETURNING clause can be specified which will return all columns.

## UPDATE

Syntax:

```
UPDATE table_name
SET column1 = value1,
    column2 = value2,
    ...
WHERE condition;
```

WHERE is optional, otherwise will update all rows in table.

RETURNING clause can also be specified:

```
UPDATE table_name
SET column1 = value1,
    column2 = value2,
    ...
WHERE condition
RETURNING * | output_expression AS output_name;
```

Returns number of updated rows.

Condition can use any math operators like <>=!

## UPDATE JOIN

Sometimes, you need to update data in a table based on values in another table. In this case, you can use the PostgreSQL UPDATE join, syntax:

```
UPDATE t1
SET t1.c1 = new_value
FROM t2
WHERE t1.c2 = t2.c2;
```

To join to another table in the UPDATE statement, you specify the joined table in the FROM clause and provide the join condition in the WHERE clause. The FROM clause must appear immediately after the SET clause.

Example:

```
UPDATE product
SET net_price = price - price * discount
FROM product_segment
WHERE product.segment_id = product_segment.id;
```

Updating values in first table, joining on second table. Table aliases can be used.

## DELETE

The PostgreSQL DELETE statement allows you to delete one or more rows from a table.

Syntax:

```
DELETE FROM table_name
WHERE condition
RETURNING (select_list | *)
```

Example of using list:

```
DELETE FROM links
WHERE id IN (6,5)
RETURNING *;
```

Note that comparison operators can be used in WHERE condition.

## DELETE JOIN

PostgreSQL doesn’t support the DELETE JOIN statement. However, it does support the USING clause in the DELETE statement that provides similar functionality as the DELETE JOIN.

Syntax:

```
DELETE FROM table_name1
USING table_expression
WHERE condition
RETURNING returning_columns;
```

Used to delete from one table based on data in another column.

Syntax:

```
DELETE FROM t1
USING t2
WHERE t1.id = t2.id
```

It can be replaced by using a SUBQUERY in WHERE, with IN. This is standard SQL and might be required for applications which must be compatible with all other SQL databases.

## UPSERT - INSERT ON CONFLICT

In relational databases, the term upsert is referred to as merge. The idea is that when you insert a new row into the table, PostgreSQL will update the row if it already exists, otherwise, it will insert the new row. That is why we call the action is upsert (the combination of update or insert).

Combination of update or insert.

```
INSERT INTO table_name(column_list) 
VALUES(value_list)
ON CONFLICT target action;
```

target:

* (column_name)
* ON CONSTRAINT constraint_name
* WHERE predicate

action:

* DO NOTHING
* DO UPDATE SET column_1 = value_1, .. WHERE condition

See source for more info and examples. Quite simple.

https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-upsert/

# Transaction

BEGIN, COMMIT and ROLLBACK

A database transaction is a single unit of work that consists of one or more operations.

A PostgreSQL transaction is atomic, consistent, isolated, and durable. These properties are often referred to as ACID:

By default, transactions are handled automatically, but can be manually controlled using BEGIN, COMMIT, ROLLBACK.

Starting a transaction with BEGIN is like beginning a session of work. Changes can be seen inside the transaction before they have been committed, but not from a different transaction.

Committing a change, COMMIT, will make the change permanent in the database.

Transactions can be used to ensure that several queries are committed to the database at the same time.

# Import and export data

## Import CSV file to table

Prepare table with correct column.

```
CREATE TABLE persons (
  id SERIAL,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  dob DATE,
  email VARCHAR(255),
  PRIMARY KEY (id)
)
```

```
COPY persons(first_name, last_name, dob, email)
FROM 'C:\sampledb\persons.csv'
DELIMITER ','
CSV HEADER;
```

Use of CSV HEADER to specify and ignore header in CSV file.

Must be on local machine, must have sudo access to copy.

## Export table to CSV

Syntax:

```
COPY persons TO 'C:\tmp\persons_db.csv' DELIMITER ',' CSV HEADER;
```

Alternative with only some columns:

```
COPY persons(first_name,last_name,email) 
TO 'C:\tmp\persons_partial_db.csv' DELIMITER ',' CSV HEADER;
```

HEADER can be excluded to not save the header.

# Managing tables

## Data types

Bool. Several different input available, return is true, false, null.

Character. CHAR(n), string, adds padding, VARCHAR(n) does not pad with spaces, TEXT variable length, unlimited length.

Numeric, integers and floats. Several types for both.

Temporal time types. Different types.

Arrays. Can store array of strings, ints, etc. in array columns.

JSON. Two types. Plain text, binary.

UUID.

Other misc types such as geometry types.

## CREATE TABLE

Syntax:

```
CREATE TABLE [IF NOT EXISTS] table_name (
   column1 datatype(length) column_contraint,
   column2 datatype(length) column_contraint,
   column3 datatype(length) column_contraint,
   table_constraints
);
```

IF NOT EXISTS can be used to skip creating the table if it already exists.

Constraints:

* NOT NULL
* UNIQUE, values in column is unique across the rows within the same table
* PRIMARY KEY, primary key for table
* CHECK, data must satisfy boolean
* FOREIGN KEY, Value in column or group of columns from a table exists in a column or group in another table

Leaving constraints blank will allow the value to be null.

Primary key can be specified as several columns. Example:

```
CREATE TABLE account_roles (
  user_id INT NOT NULL,
  role_id INT NOT NULL,
  grant_date TIMESTAMP,
  PRIMARY KEY (user_id, role_id),
  FOREIGN KEY (role_id)
      REFERENCES roles (role_id),
  FOREIGN KEY (user_id)
      REFERENCES accounts (user_id)
);
```

Because user_id references a column in another table we need to define a foreign key constraint with the REFERENCES keyword.

## SELECT INTO


