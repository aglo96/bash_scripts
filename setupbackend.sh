#!/bin/bash

# cd ~
# sudo apt-get update
# # git clone --single-branch --branch ag https://github.com/skimkoh/bigdata-goodreads.git
# git clone https://github.com/skimkoh/bigdata-goodreads.git

# sudo apt-get install nginx
# sudo apt-get install gunicorn3
# # cd /etc/nginx/sites-enabled/

# echo "Setting up nginx"

ipaddress=$(curl http://checkip.amazonaws.com)


cat > /etc/nginx/sites-enabled/flaskapp <<EOF 
server {
        listen 80;
        server_name $ipaddress;

        location / {
                proxy_pass http://127.0.0.1:8000;
        }
}
EOF

sudo service nginx restart


# cd bigdata-goodreads/backend
# sudo apt-get install python3-venv
# python3 -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt
# gunicorn -w 4 application

# echo "backend server is up"