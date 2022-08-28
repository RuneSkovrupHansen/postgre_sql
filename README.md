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
* \d <relation> - show relation info, by default shows current db info
* \dt <table_name> - Shows list of tables in db
* \ds <sequence> - Shows list of sequences in db

In general, it seems that \d is some query prefix which can be extended for specific targets, such as tables or sequences, etc.

\d = details, can be used with any relation such as a table. Shows the details about that relation.

\d+ offers additional details.

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

Another example:

```
WITH category_with_names AS (SELECT film_id, name FROM film_category INNER JOIN category USING(category_id))
SELECT f.title, c.name category FROM film f INNER JOIN category_with_names c USING(film_id);
```

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

The PostgreSQL SELECT INTO statement creates a new table and inserts data returned from a query into the table.

The new table will have columns with the names the same as columns of the result set of the query. Unlike a regular SELECT statement, the SELECT INTO statement does not return a result to the client.

Syntax:

```
SELECT
    select_list
INTO [ TEMPORARY | TEMP | UNLOGGED ] [ TABLE ] new_table_name
FROM
    table_name
WHERE
    search_condition;
```

Example:

```
SELECT
    film_id,
    title,
    rental_rate
INTO TABLE film_r
FROM
    film
WHERE
    rating = 'R'
AND rental_duration = 5
ORDER BY
    title;
```

## CREATE TABLE AS

The CREATE TABLE AS statement creates a new table and fills it with the data returned by a query.

Syntax:

```
CREATE [ <Nothing> | TEMPORARY | UNLOGGED ] TABLE new_table_name
AS query;
```

```
CREATE TABLE IF NOT EXISTS new_table_name
AS query;
```

Example:

```
CREATE TABLE action_film AS
SELECT
    film_id,
    title,
    release_year,
    length,
    rating
FROM
    film
INNER JOIN film_category USING (film_id)
WHERE
    category_id = 1;
```

Preferred to SELECT INTO.

Example:

```
CREATE TABLE IF NOT EXISTS film_rating (rating, film_count) 
AS 
SELECT
    rating,
    COUNT (film_id)
FROM
    film
GROUP BY
    rating;
```

## SERIAL to create auto-increment column

In PostgreSQL, a sequence is a special kind of database object that generates a sequence of integers. A sequence is often used as the primary key column in a table.

When creating a new table, the sequence can be created through the SERIAL pseudo-type.

Pseudo-type that can be assigned to a column. When assigned:

* Creates sequence object and assigns it to column
* Generate default values from sequence
* Set column to not null

Commonly used to id columns. Example:

```
CREATE TABLE table_name(
    id SERIAL
);
```

Equivalent to:

```
CREATE SEQUENCE table_name_id_seq;

CREATE TABLE table_name (
    id integer NOT NULL DEFAULT nextval('table_name_id_seq')
);

ALTER SEQUENCE table_name_id_seq
OWNED BY table_name.id;
```

Different types of serials for different number of expected ids.

Does not make column primary key, but that can be added. Example:

```
CREATE TABLE fruits(
   id SERIAL PRIMARY KEY,
   name VARCHAR NOT NULL
);
```

To assign default values use DEFAULT or omit the column from a statement. Example:

```
INSERT INTO fruits(id,name) 
VALUES(DEFAULT,'Orange');
```

Get recent value generated by sequencer:

`SELECT currval(pg_get_serial_sequence('fruits', 'id'));`

## Sequences

A PostgreSQL sequence object can be used to generate a sequence of numbers.

By definition, a sequence is an ordered list of integers. The orders of numbers in the sequence are important. For example, {1,2,3,4,5} and {5,4,3,2,1} are entirely different sequences.

### Create

CREATE SEQUENCE statement.

```
CREATE SEQUENCE [ IF NOT EXISTS ] sequence_name
    [ AS { SMALLINT | INT | BIGINT } ]
    [ INCREMENT [ BY ] increment ]
    [ MINVALUE minvalue | NO MINVALUE ] 
    [ MAXVALUE maxvalue | NO MAXVALUE ]
    [ START [ WITH ] start ] 
    [ CACHE cache ] 
    [ [ NO ] CYCLE ]
    [ OWNED BY { table_name.column_name | NONE } ]
```

See source for details on options. https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-sequences/.

Creating a sequence:

```
CREATE SEQUENCE mysequence
INCREMENT 5
START 100;
```

### Use

Get value from sequence:

`SELECT nextval('mysequence');`


Creating a sequence associated with a table column:

```
CREATE TABLE order_details(
    order_id SERIAL,
    item_id INT NOT NULL,
    item_text VARCHAR NOT NULL,
    price DEC(10,2) NOT NULL,
    PRIMARY KEY(order_id, item_id)
);
```

```
CREATE SEQUENCE order_item_id
START 10
INCREMENT 10
MINVALUE 10
OWNED BY order_details.item_id;
```

Use to generate values in queries:

```
INSERT INTO 
    order_details(order_id, item_id, item_text, price)
VALUES
    (100, nextval('order_item_id'),'DVD Player',100),
    (100, nextval('order_item_id'),'Android TV',550),
    (100, nextval('order_item_id'),'Speaker',250);
```

Even if the sequence is owned by a column it is not evoked by default to create default values. Default values could probably be specified to use the sequence.

### Delete

Syntax:

```
DROP SEQUENCE [ IF EXISTS ] sequence_name [, ...] 
[ CASCADE | RESTRICT ];
```

CASCADE will delete objects that depend on the sequence recursively.

## Identity Column

The GENERATED AS IDENTITY constraint is the SQL standard-conforming variant of the good old SERIAL column.

Syntax:

`column_name type GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY[ ( sequence_option ) ]`

Like the SERIAL, the GENERATED AS IDENTITY constraint also uses the SEQUENCE object internally.

Seems to be another serial-like specifier to generate values for a column in a table. Adheres to a SQL standard.

ALWAYS will enforce that the value is **always** generated by the sequences. Trying to manually specify requires system override.

BY DEFAULT will only generate values from sequence when the value is generated as the default. Manually specifying is possible without override.

Table creation with BY DEFAULT example:

```
DROP TABLE color;

CREATE TABLE color (
    color_id INT GENERATED BY DEFAULT AS IDENTITY,
    color_name VARCHAR NOT NULL
);
```

Using sequence_option example:

```
DROP TABLE color;

CREATE TABLE color (
    color_id INT GENERATED BY DEFAULT AS IDENTITY 
    (START WITH 10 INCREMENT BY 10),
    color_name VARCHAR NOT NULL
); 
```

Adding identity column to an existing table:

```
ALTER TABLE table_name 
ALTER COLUMN column_name 
ADD GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY { ( sequence_option ) }
```

Cannot be added to nullable column.

\d will show ALWAYS / BY DEFAULT

See source for info on how to alter and remove from existing columns.

https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-identity-column/

## ALTER TABLE

Source contains several in-depth examples for each action.

To change the structure of an existing table, you use PostgreSQL ALTER TABLE statement.

Syntax:

`ALTER TABLE table_name action;`

Many different options, add column, rename column, set / drop default, etc.

Add syntax:

```
ALTER TABLE table_name 
ADD COLUMN column_name datatype column_constraint;
```

Example of adding constraint:

```
ALTER TABLE links 
ADD CONSTRAINT unique_url UNIQUE ( url );
```

INSERT statements with duplicate URLs will fail and cause an error.

## RENAME TABLE

When you rename a table to the new one, PostgreSQL will automatically update its dependent objects such as foreign key constraints, views, and indexes.

## ADD COLUMNS

Multiple can be added, example:

```
ALTER TABLE table_name
ADD COLUMN column_name1 data_type constraint,
ADD COLUMN column_name2 data_type constraint,
...
ADD COLUMN column_namen data_type constraint;
```

It is not possible to add a column with NOT NULL since values will be NULL be default. Create as nullable, fill in data, and then set it as NOT NULL.

## REMOVE COLUMNS

Syntax:

```
ALTER TABLE table_name 
DROP COLUMN [IF EXISTS] column_name [CASCADE];
```

CASCADE can be used to drop all dependent objects, such as views, sequences, etc.

Cannot drop objects without CASCADE if other objects depend on it.

## Change column type

Syntax:

```
ALTER TABLE table_name
ALTER COLUMN column_name1 [SET DATA] TYPE new_data_type,
ALTER COLUMN column_name2 [SET DATA] TYPE new_data_type,
...;
```

SET DATA is optional.

Possible to convert values while changing data type, syntax:

```
ALTER TABLE table_name
ALTER COLUMN column_name TYPE new_data_type USING expression;
```

USING expression specifies conversion. Omitting USING PostgreSQL will try to cast values implicitly, if it fails, Postgres will throw an error.

Seems to be specific cast expressions which can be used. Example:

```
ALTER TABLE assets
ALTER COLUMN asset_no TYPE INT 
USING asset_no::integer;
```

## RENAME COLUMN

Syntax:

```
ALTER TABLE table_name 
RENAME column_name TO new_column_name;
```

IF EXISTS cannot be used, cannot rename multiple columns at once.

When renaming, all dependent objects will have references updated.

## DROP TABLE

Syntax:

```
DROP TABLE [IF EXISTS] table_name 
[CASCADE | RESTRICT];
```

The RESTRICT option rejects the removal if there is any object depends on the table. The RESTRICT option is the default if you don’t explicitly specify it in the DROP TABLE statement.

Multiple tables can be specified.

## TRUNCATE TABLE

To remove all data from a table, you use the DELETE statement. However, when you use the DELETE statement to delete all data from a table that has a lot of data, it is not efficient. In this case, you need to use the TRUNCATE TABLE statement.

Syntax:

`TRUNCATE TABLE table_name;`

The  TRUNCATE TABLE statement deletes all data from a table without scanning it. This is the reason why it is faster than the DELETE statement.

In addition, the TRUNCATE TABLE statement reclaims the storage right away so you do not have to perform a subsequent VACUMM operation, which is useful in the case of large tables.

DELETE to delete data. TRUNCATE to delete all data. DROP to remove table.

```
TRUNCATE TABLE table_name 
RESTART IDENTITY;
```

RESTART IDENTITY can be used to restart seqeunce.

Multiple tables can be specified. CASCADE is available.

Does not fire ON DELETE triggers, must be specified with BEFORE TRUNCATE and AFTER TRUNCATE triggers.

Transaction safe - Can be rolled back in a transaction.

## Temporary Table

A temporary table, as its named implied, is a short-lived table that exists for the duration of a database session. PostgreSQL automatically drops the temporary tables at the end of a session or a transaction.

Syntax:

```
CREATE TEMP TABLE temp_table(
   ...
);
```

A temporary table is visible only to the session that creates it. In other words, it is invisible to other sessions.

Temporary tables are listed under tables however they are under a temp schema.

Can have same name as existing tables but it is not recommended.

Dropped as regular tables.

## Copy Table

```
CREATE TABLE new_table AS 
TABLE existing_table 
WITH NO DATA;
```

If WITH NO DATA is not specified, data is copied.

To partially copy data the CREATE TABLE <name> AS can be used.

# PostgreSQL Constraints

## Primary key

A primary key is a column or a group of columns used to identify a row uniquely in a table.

You define primary keys through primary key constraints. Technically, a primary key constraint is the combination of a not-null constraint and a UNIQUE constraint.

Syntax:

```
CREATE TABLE TABLE (
	column_1 data_type PRIMARY KEY,
	column_2 data_type,
	…
);
```

```
CREATE TABLE TABLE (
	column_1 data_type,
	column_2 data_type,
	… 
        PRIMARY KEY (column_1, column_2)
);
```

If no name is specified for PRIMARY KEY postgres will specify a default key.

Change primary key, syntax:

`ALTER TABLE table_name ADD PRIMARY KEY (column_1, column_2);`

How to remove primary key constraint, syntax:

`ALTER TABLE table_name DROP CONSTRAINT primary_key_constraint;`

## FOREIGN KEY

A foreign key is a column or a group of columns in a table that reference the primary key of another table.

The table that contains the foreign key is called the referencing table or child table. And the table referenced by the foreign key is called the referenced table or parent table.

In PostgreSQL, you define a foreign key using the foreign key constraint. The foreign key constraint helps maintain the referential integrity of data between the child and parent tables.

A foreign key constraint indicates that values in a column or a group of columns in the child table equal the values in a column or a group of columns of the parent table.

Syntax:

```
[CONSTRAINT fk_name]
   FOREIGN KEY(fk_columns) 
   REFERENCES parent_table(parent_key_columns)
   [ON DELETE delete_action]
   [ON UPDATE update_action]
```

Several optional parts of the statement.

A foreign key is the primary key in a different table. Rarely updated, sometimes deleted.

Following actions:

* SET NULL
* SET DEFAULT
* RESTRICT
* NO ACTION
* CASCADE

Default is NO ACTION. NO ACTION causes a constraint violation error when the element is deleted.

CASCADE deletes rows affected.

Example:

```
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS contacts;

CREATE TABLE customers(
   customer_id INT GENERATED ALWAYS AS IDENTITY,
   customer_name VARCHAR(255) NOT NULL,
   PRIMARY KEY(customer_id)
);

CREATE TABLE contacts(
   contact_id INT GENERATED ALWAYS AS IDENTITY,
   customer_id INT,
   contact_name VARCHAR(255) NOT NULL,
   phone VARCHAR(15),
   email VARCHAR(100),
   PRIMARY KEY(contact_id),
   CONSTRAINT fk_customer
      FOREIGN KEY(customer_id) 
	  REFERENCES customers(customer_id)
);
```

Add constraint to existing table, syntax:

```
ALTER TABLE child_table 
ADD CONSTRAINT constraint_name 
FOREIGN KEY (fk_columns) 
REFERENCES parent_table (parent_key_columns);
```

See source for adding CASCADE constraint to existing table.

## CHECK

A CHECK constraint is a kind of constraint that allows you to specify if values in a column must meet a specific requirement.

The CHECK constraint uses a Boolean expression to evaluate the values before they are inserted or updated to the column.

If the values pass the check, PostgreSQL will insert or update these values to the column. Otherwise, PostgreSQL will reject the changes and issue a constraint violation error.

Example:

```
DROP TABLE IF EXISTS employees;
CREATE TABLE employees (
	id SERIAL PRIMARY KEY,
	first_name VARCHAR (50),
	last_name VARCHAR (50),
	birth_date DATE CHECK (birth_date > '1900-01-01'),
	joined_date DATE CHECK (joined_date > birth_date),
	salary numeric CHECK(salary > 0)
);
```

Possible to set custom names.

Example, adding CHECK to existing table:

```
ALTER TABLE prices_list 
ADD CONSTRAINT price_discount_check 
CHECK (
	price > 0
	AND discount >= 0
	AND price > discount
);
```

AND can be used inside of the check.

## UNIQUE

When a UNIQUE constraint is in place, every time you insert a new row, it checks if the value is already in the table. It rejects the change and issues an error if the value already exists. The same process is carried out for updating existing data.

Table can be made unique on several columns at once, syntax:

```
CREATE TABLE table (
    c1 data_type,
    c2 data_type,
    c3 data_type,
    UNIQUE (c2, c3)
);
```

Adding to table requires a lock on the table.

## NOT NULL

In database theory, NULL represents unknown or information missing. NULL is not the same as an empty string or the number zero.

NULL is very special. It does not equal anything, even itself. The expression NULL = NULL returns NULL because it makes sense that two unknown values should not be equal.

Updating or inserting to NULL with a NOT NULL constraint will cause a constraint error.

Example:

```
CREATE TABLE invoices(
  id SERIAL PRIMARY KEY,
  product_id INT NOT NULL,
  qty numeric NOT NULL CHECK(qty > 0),
  net_price numeric CHECK(net_price > 0) 
);
```

Adding to existing, syntax:

```
ALTER TABLE table_name
ALTER COLUMN column_name_1 SET NOT NULL,
ALTER COLUMN column_name_2 SET NOT NULL,
...;
```

Equivalent to CHECK(col IS NOT NULL)

# Data types

## Boolean

true, false, NULL

Several synonyms.

WHERE <bool_column> can be used.

NOT to negate in WHERE clauses.

## Character types

* VARCHAR(n) - variable-length with length limit
* CHAR(n) - fixed-length, blank padded
* TEXT/VARCHAR - variable unlimited length

More synonyms.

## Numeric

The NUMERIC type can store numbers with a lot of digits. Typically, you use the NUMERIC type for numbers that require exactness such as monetary amounts or quantities.

Syntax:

`NUMERIC(precision, scale)`

In this syntax, the precision is the total number of digits and the scale is the number of digits in the fraction part. For example, the number 1234.567 has the precision 7 and scale 3.

Numeric can also hold NaN.

## Integers

Different types:

* SMALLINT
* INTEGER
* BIGINT

Does not provide unsigned int, unlike MySQL.

Can add CHECK constraint to ensure only positive or negative values are inserted into a column.

Choose only what is required. Overestimating degrades the performance of the database.

## Dates

DATE, yyyy-mm-dd

After DEFAULT constraint, CURRENT_DATE can be specified to insert current data.

NOW() can be used to get current date and time, NOW()::date can be used to get only the current date.

SELECT CURRENT_DATE also gets the current date.

Different ways to output a date:

`SELECT TO_CHAR(NOW() :: DATE, 'dd/mm/yyyy');` - 12/06/1993
`SELECT TO_CHAR(NOW() :: DATE, 'Mon dd, yyyy');` - Jun 12, 1993

Intervals between two dates can be retrieved using the - operator. Example:

```
SELECT
	first_name,
	last_name,
	now() - hire_date as diff
FROM
	employees;
```

To calculate age at the current date in years, months, and days, you use the AGE() function. Example:

```
SELECT
	employee_id,
	first_name,
	last_name,
	AGE(birth_date)
FROM
	employees;
```

More arguments can be passed.

Individual pieces of info can be extracted from a DATE, example:

```
SELECT
	employee_id,
	first_name,
	last_name,
	EXTRACT (YEAR FROM birth_date) AS YEAR,
	EXTRACT (MONTH FROM birth_date) AS MONTH,
	EXTRACT (DAY FROM birth_date) AS DAY
FROM
	employees;
```

## Timestamps

* timestamp - timestamp without timezone
* timestamptz - timestamp with a timezone

Without timezone the database timestamp values will not change depending on the time zone of the server.

Timezone stored in UTC value. When a value is stored in a timestamptz, the value is converted to UTC and stored. The value is reversed when a timestamptz data is queried, transformed into the timezone of the server.

Timezone of the database server can be set using:

`SET timezone = 'America/Los_Angeles';`

`SHOW TIMEZONE;`

Generally, it is a good practice to use the timestamptz datatype to store the timestamp data.

Get timestamp:

`SELECT NOW();`

`SELECT CURRENT_TIMESTAMP;`

`SELECT TIMEOFDAY();`

Convert timestamp manually:

SELECT timezone(<timezone>, <timestamp>)

## Interval

The interval data type allows you to store and manipulate a period of time in years, months, days, hours, minutes, seconds, etc.

`[ @ ] interval [ fields ] [ (p) ]`

p is used for precision.

Useful for date and time calculations. Example:

```
SELECT
	now(),
	now() - INTERVAL '1 year 3 hours 20 minutes' 
             AS "3 hours 20 minutes ago of last year";
```

Several units can be used. Alternate syntax follows ISO standard.

`P [ years-months-days ] [ T hours:minutes:seconds ]`

Output type of Postgres can be specified with command.

`SET intervalstyle = 'sql_standard';`

Can be converted to characters using TO_CHAR().

EXTRACT() can be called to get specific parts of an interval.

## Time data type

PostgreSQL provides the TIME data type that allows you to store the time of day values.

Syntax:

`column_name TIME(precision);`

`column TIME with time zone`

Different formats. Different ways to get current TIME.

Timezones can also be loaded.

Math with other time formats can be performed. Adding an interval example.

## UUID

UUID stands for Universal Unique Identifier defined by RFC 4122 and other related standards. A UUID value is 128-bit quantity generated by an algorithm that make it unique in the known universe using the same algorithm.

Because of its uniqueness feature, you often found UUID in the distributed systems because it guarantees a better uniqueness than the SERIAL data type which generates only unique values within a single database.

Extension "uuid-ossp" must be installed to generate UUIDs.

`CREATE EXTENSION IF NOT EXISTS "uuid-ossp";`

To generate based on MAC address:

`SELECT uuid_generate_v1();`

Generate purely random:

`SELECT uuid_generate_v4();`


Using UUID as primary key example:

```
CREATE TABLE contacts (
    contact_id uuid DEFAULT uuid_generate_v4 (),
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    phone VARCHAR,
    PRIMARY KEY (contact_id)
);
```

## Array

Array plays an important role in PostgreSQL. Every data type has its own companion array type e.g., integer has an integer[] array type, character has character[] array type, etc. In case you define your own data type, PostgreSQL creates a corresponding array type in the background for you.

Array for each data type.

Text array, example:

```
CREATE TABLE contacts (
	id serial PRIMARY KEY,
	name VARCHAR (100),
	phones TEXT []
);  
```

When inserting, either [] or {} is used.

Example:

```
INSERT INTO contacts (name, phones)
VALUES('Lily Bush','{"(408)-589-5841"}'),
      ('William Gate','{"(408)-589-5842","(408)-589-58423"}');
```

Postgres is one-based, arrays start at 1. Indexing is as normal, example:

```
SELECT
	name,
	phones [ 1 ]
FROM
	contacts;
```

Can be used in WHERE clause.

ANY() can be used to search to check if any value matches in the array. Example:

```
SELECT
	name,
	phones
FROM
	contacts
WHERE
	'(408)-589-5555' = ANY (phones);
```

unnest() to expand array into list of rows. Will return multiple rows for each entry in an array.

## hstore

The hstore module implements the hstore data type for storing key-value pairs in a single value.

The hstore data type is very useful in many cases, such as semi-structured data or rows with many attributes that are rarely queried. Notice that keys and values are just text strings only.

External module:

`CREATE EXTENSION hstore;`

Example:

```
CREATE TABLE books (
	id serial primary key,
	title VARCHAR (255),
	attr hstore
);
```

```
INSERT INTO books (title, attr)
VALUES
	(
		'PostgreSQL Tutorial',
		'"paperback" => "243",
	   "publisher" => "postgresqltutorial.com",
	   "language"  => "English",
	   "ISBN-13"   => "978-1449370000",
		 "weight"    => "11.2 ounces"'
	);
```

Inserting values into the attr, note that the key-value pairs are comma separated and wrapped in single quotes.

Querying the hstore column you will get all values, but it's possible to select specific keys. Example:

```
SELECT
	attr -> 'ISBN-13' AS isbn
FROM
	books;
```

-> '<key>' to get specific key.

Updating a value, example:

```
UPDATE books
SET attr = attr || '"freeshipping"=>"no"' :: hstore;
```

Removing a pair, example:

```
UPDATE books 
SET attr = delete(attr, 'freeshipping');
```

Check for key in hstore column, example:

```
SELECT
  title,
  attr->'publisher' as publisher,
  attr
FROM
	books
WHERE
	attr ? 'publisher';
```

More operations, see source.

https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-hstore/

## JSON

Data type to hold JSON.

```
CREATE TABLE orders (
	id serial NOT NULL PRIMARY KEY,
	info json NOT NULL
);
```

Syntax like hstore to retrieve individual key values.

```
SELECT info -> 'customer' AS customer
FROM orders;
```

-> - Get as JSON
->> Get as text

Returned for all rows in a column.

Arrow operators can be chained for nested objects.

Advanced example:

```
SELECT info ->> 'customer' AS customer,
	info -> 'items' ->> 'product' AS product
FROM orders
WHERE CAST ( info -> 'items' ->> 'qty' AS INTEGER) = 2
```

Get customer and product from JSON where items qty was 2.

Casts must be used since JSON is just text.

Aggregation functions example:

```
SELECT 
   MIN (CAST (info -> 'items' ->> 'qty' AS INTEGER)),
   MAX (CAST (info -> 'items' ->> 'qty' AS INTEGER)),
   SUM (CAST (info -> 'items' ->> 'qty' AS INTEGER)),
   AVG (CAST (info -> 'items' ->> 'qty' AS INTEGER))
FROM orders;
```

Some unique JSON functions exist, to get keys only, etc.

## User-defined data typed

CREATE DOMAIN and CREATE TYPE.

Besides built-in data types, PostgreSQL allows you to create user-defined data types through the following statements:

* CREATE DOMAIN creates a user-defined data type with constraints such as NOT NULL, CHECK, etc.
* CREATE TYPE creates a composite type used in stored procedures as the data types of returned values.

Example of creating a domain, to replace constraints:

```
CREATE DOMAIN contact_name AS 
   VARCHAR NOT NULL CHECK (value !~ '\s');
```

The check is probably for spacing, \s.

The domain is used as constraints when creating a table, for columns first_name and last_name.

```
CREATE TABLE mailing_list (
    id serial PRIMARY KEY,
    first_name contact_name,
    last_name contact_name,
    email VARCHAR NOT NULL
);
```

Create type:

```
CREATE TYPE film_summary AS (
    film_id INT,
    title VARCHAR,
    release_year SMALLINT
); 
```

Use type as part of function, as the return type:

```
CREATE OR REPLACE FUNCTION get_film_summary (f_id INT) 
    RETURNS film_summary AS 
$$ 
SELECT
    film_id,
    title,
    release_year
FROM
    film
WHERE
    film_id = f_id ; 
$$ 
LANGUAGE SQL;
```

Usage:

`SELECT * FROM get_film_summary (40);`

# Conditional expressions and operators

## CASE

The PostgreSQL CASE expression is the same as IF/ELSE statement in other programming languages. It allows you to add if-else logic to the query to form a powerful query.

Two forms, general and simple.

General:

```
CASE 
      WHEN condition_1  THEN result_1
      WHEN condition_2  THEN result_2
      [WHEN ...]
      [ELSE else_result]
END
```

Evaluates conditions top -> bottom to find condition that is true.

Stops at first true condition.

Example:

```
SELECT title,
       length,
       CASE
           WHEN length> 0
                AND length <= 50 THEN 'Short'
           WHEN length > 50
                AND length <= 120 THEN 'Medium'
           WHEN length> 120 THEN 'Long'
       END duration
FROM film
ORDER BY title;
```

Simple:

```
CASE expression
   WHEN value_1 THEN result_1
   WHEN value_2 THEN result_2 
   [WHEN ...]
ELSE
   else_result
END
```

## COALESCE

Syntax:

`COALESCE (argument_1, argument_2, …);`

Returns first argument that is not null.

Example:

```
SELECT
	COALESCE (NULL, 2 , 1);
```

Evaluates to 2.

Example:

```
SELECT
	product,
	(price - COALESCE(discount,0)) AS net_price
FROM
	items;
```

Handles cases where discount is NULL.

## ISNULL

`ISNULL(expression, replacement)`

Used to replace null values. Similar to COALESCE. Can also be replaced using CASE.

## NULLIF

`NULLIF(argument_1,argument_2);`

The NULLIF function returns a null value if argument_1 equals to argument_2, otherwise it returns argument_1.

Example usage:

`NULLIF (description, '')`

Common usage is to guard against null division.

## CAST

There are many cases that you want to convert a value of one data type into another. PostgreSQL provides you with the CAST operator that allows you to do this.

`CAST ( expression AS target_type );`

Alternate simpler syntax:

`expression::type`

Example:

```
SELECT
  '100'::INTEGER,
  '01-OCT-2015'::DATE;
```

If the expression cannot be converted to the target type, PostgreSQL will raise an error.

Examples for all data types.

# psql

## Connect to db

`psql -d database -U  user -W`
`psql -h host -d database -U user -W` - Connect to remote host db

## Switch to new db

`\c dbname username`

## List commands

List commands

* `\d` - dbs
* `\dt` - tables
* `\dn` - schema
* `\df` - functions
* `\dv` - views
* `\du` - roles

## Previous command

`\g` - show command history

## History

`\s` - command history

## Execute from file

`\i filename` - execute from file

## Help on statements

`\h statement` - help on statement

## Timing

How much time a query takes

`\timing` - enable / disable timing

## Editor

`\e` - open editor to write query in
`\ef function_name` - edit function from editor

## Quit

`\q`

# PostgreSQL Recipes

## Generate random number

`SELECT random();`

`SELECT random() * 10 + 1 AS RAND_1_11;`

Can use floor() to force integer value, example:

`SELECT floor(random() * 10 + 1)::int;`

Can create function to return random number.

## Delete duplicate rows

Example:

```
DELETE FROM
    basket a
        USING basket b
WHERE
    a.id < b.id
    AND a.fruit = b.fruit;
```

## EXPLAIN

The EXPLAIN statement returns the execution plan which PostgreSQL planner generates for a given statement.

The EXPLAIN shows how tables involved in a statement will be scanned by index scan or sequential scan, etc., and if multiple tables are used, what kind of join algorithm will be used.

`EXPLAIN [ ( option [, ...] ) ] sql_statement;`

Several options.

Example:

`EXPLAIN SELECT * FROM film;`

## PostgreSQL vs MySQL

Postgres has more advanced functions but is not as easy to use as MySQL.

See source for details.

https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-vs-mysql/