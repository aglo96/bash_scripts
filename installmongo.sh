#!/bin/bash


sudo apt-get update
sudo apt install unzip
wget -c https://istd50043.s3-ap-southeast-1.amazonaws.com/kindle-reviews.zip -O kindle-reviews.zip
unzip kindle-reviews.zip
rm -rf kindle_reviews.json

wget -c https://istd50043.s3-ap-southeast-1.amazonaws.com/meta_kindle_store.zip -O meta_kindle_store.zip
unzip meta_kindle_store.zip
rm -rf *.zip



wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -

sudo apt-get install gnupg

wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -

echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list

sudo apt-get update

sudo apt-get install -y mongodb-org

sudo service mongod start

# sudo sed -i "s/.*bindIp.*/  bindIp = 0.0.0.0/" /etc/mongod.conf

# sudo service mongod restart




# sudo service mongod start



