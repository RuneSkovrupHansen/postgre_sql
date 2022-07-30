#!/bin/bash

rm dvdrental.zip dvdrental.tar

curl -O https://www.postgresqltutorial.com/wp-content/uploads/2019/05/dvdrental.zip
unzip dvdrental.zip

sudo apt-get install postgresql

# Install pip requirements
pip install -r requirements.txt

echo "setup finished, please remember to update authentication method for psql" 