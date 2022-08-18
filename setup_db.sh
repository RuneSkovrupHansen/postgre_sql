#!/bin/bash

# Set up dvdrental database

rm -f dvdrental.zip
rm -f dvdrental.tar

curl -LO https://www.postgresqltutorial.com/wp-content/uploads/2019/05/dvdrental.zip
unzip dvdrental.zip

sudo apt-get install postgresql

sudo service postgresql start

sudo -u postgres psql -c "drop database dvdrental;"
sudo -u postgres psql -c "create database dvdrental;"

sudo -u postgres pg_restore --dbname=dvdrental dvdrental.tar

echo "Database has been set up, please remember to check authentication"