# sudo apt-get update
# sudo apt-get -y install nodejs npm

sudo apt-get -y install nginx 

echo "Setting up nginx"
sudo chmod o+rw /etc/nginx/sites-enabled

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

# # git clone https://github.com/skimkoh/bigdata-goodreads.git
# cd bigdata-goodreads/frontend
# npm install  #npm install dosen't work on t2.micro. Not enough RAM
# npm start

# base_api=$(sed -n 's/backend \(.*\)/\1/p' < ec2InstancesProductionSystem.txt | awk '{print $2}')
# echo $base_api

echo "frontend server is up"