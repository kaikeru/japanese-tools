#! /usr/bin/env bash

# Run as ROOT

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )


apt install python3.9
apt install sqlite3
apt install nginx

litestream_version="0.3.9"
wget https://github.com/benbjohnson/litestream/releases/download/v$litestream_version/litestream-v$litestream_version-linux-amd64.deb
dpkg -i litestream-v$litestream_version-linux-amd64.deb
rm litestream-v$litestream_version-linux-amd64.deb


cd $SCRIPT_DIR/../../

python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements

deactivate

# Copy configs
cd $SCRIPT_DIR/../server_files
cp ./etc/nginx/sites-avilable/japanese-tools /etc/nginx/sites-avilable/japanese-tools
ln -s /etc/nginx/sites-avilable/japanese-tools /etc/nginx/sites-enabled/

cp ./etc/systemd/systems/gunicorn.service /etc/systemd/systems/gunicorn.service

cp ./etc/litestream.yml /etc/litestream.yml

# Start services

systemctl enable gunicorn
systemctl start gunicorn

systemctl enable nginx
systemctl start nginx

systemctl enable litestream
systemctl start litestream
