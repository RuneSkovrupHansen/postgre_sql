# postgre_sql
Repository for playing around with PostgreSQL

sudo service postgresql status
sudo service postgresql start
sudo service postgresql stop

Connect to the postgres service and open the psql shell:

    sudo -u postgres psql

psql – a terminal-based front-end to PostgreSQL database server

It is possible to specify server host or socket directory and port of the server, while calling psql to connect to a database.

CREATE DATABASE dvdrental;

postgres=# \conninfo


## Connection

By default, connection to a local server is established through a socket. This seems to have several side effects.

Note that in the commands above, we're actually specifying using sudo, that the user should be set to postgres before the psql command is run. This ensures that we log in as postgres.

    sudo -u postgres psql

### Authentication

Different methods of authentication. Can be specified for the types of connection. For Unix domain socket the default is "peer" which pulls the username from the system.

https://stackoverflow.com/a/18664239/13308972

For example, changing peer to password, it's possible to connect using the command:

psql -U postgres -W

This command explicitly sets the user to "postgres" and forces a password prompt. Since the user info is no longer pulled by the system, this command works.

Another option is md5 which is more secure.

## Commands

It's possible to use both psql commands and SQL commands to control psql. It would seem that postgresql stores it's information in a postgres db as well, which is what is making this possible.

Command:

* \c <name> - connect to db
* DROP DATABASE <name> - drop db

SQL:
* select count(*) from film; - count all from table films

## Load / restore database

sudo -u postgres pg_restore -d <database> <file>

    The file must be a .tar file.

