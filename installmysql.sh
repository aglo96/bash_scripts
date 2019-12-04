#!/bin/bash


sudo apt-get update
sudo apt install unzip
unzip kindle-reviews.zip
rm -rf kindle_reviews.json

wget -c https://istd50043.s3-ap-southeast-1.amazonaws.com/meta_kindle_store.zip -O meta_kindle_store.zip
unzip meta_kindle_store.zip
rm -rf *.zip




sudo apt-get install mysql-server


sudo mysql -e 'update mysql.user set plugin = "mysql_native_password" where
user="root"'
sudo mysql -e 'create user "root"@"%" identified by ""'
sudo mysql -e 'grant all privileges on *.* to "root"@"%" with grant option'
sudo mysql -e 'flush privileges'


#need to set binding to 0.0.0.0
# cd /etc/mysql/mysql.conf.d
echo "Updating mysql configs in /etc/mysql/my.cnf."
sudo sed -i "s/.*bind-address.*/bind-address = 0.0.0.0/" /etc/mysql/mysql.conf.d/mysqld.cnf
echo "Updated mysql bind address in /etc/mysql/my.cnf to 0.0.0.0 to allow external connections."
cd ~

sudo service mysql restart


mysql -u root
create database book_reviews
use book_reviews
