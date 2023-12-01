#!/bin/bash

# Create folder required for storing log files.
mkdir -p /var/log/sugarbox/provisioningagent 

# Create folder required for edge template files and packages.
mkdir -p /opt/sugarbox/config

# Copy the defaults file required by nginx to point to our applicaton.
cp tests/default /etc/nginx/sites-available/

# Copy the config file required to the code config for tests.
cp tests/default.ini config/

# Start nginx server.
service nginx start

# Re-create database
mysql --defaults-file=tests/mysql.cnf < tests/initialdb.sql

# Move to the source folder
cd src

# Start the provisioning server.
python3 wsgi.py
