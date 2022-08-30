#! /usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd ..

git pull
sudo systemctl stop gunicorn
rm -rf venv
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic -c --no-input
deactivate
sudo systemctl start gunicorn
