#!/bin/bash

# update repos
sudo apt-get update 

# mysql config
sudo apt-get install pwgen -y
MYSQL_PASS=`pwgen -s 10`

sudo debconf-set-selections \
    <<< "mysql-server-5.0 mysql-server/root_password password $MYSQL_PASS"
sudo debconf-set-selections \
    <<< "mysql-server-5.0 mysql-server/root_password_again password $MYSQL_PASS"

MYSQL_HOST="127.0.0.1"
MYSQL_PORT="3306"
MYSQL_USER="root"
MYSQL_DB="scores"

sed -e "s#{MYSQL_PASS}#$MYSQL_PASS#g" \
    -e "s#{MYSQL_HOST}#$MYSQL_HOST#g" \
    -e "s#{MYSQL_PORT}#$MYSQL_PORT#g" \
    -e "s#{MYSQL_USER}#$MYSQL_USER#g" \
    -e "s#{MYSQL_DB}#$MYSQL_DB#g" \
    env_settings.py.template | \
    tee env_settings.py > /dev/null

# install deps
sudo apt-get install python-dev -y
sudo apt-get install mysql-server -y
sudo apt-get install python-setuptools python-mysqldb -y
sudo apt-get install curl -y ; curl -L http://cpanmin.us | perl - --self-upgrade
sudo easy_install pip
sudo easy_install pytz
sudo easy_install elementtree
sudo pip install SQLAlchemy
sudo pip install python-dateutil

# install LED sign deps
(echo y;echo o conf prerequisites_policy follow;echo o conf commit) | sudo cpanm --dev --verbose Device::MiniLED

# install supervisord
PWD=`pwd`
sed "s#{SCORES_PATH}#$PWD#g" supervisord_template.conf | \
        sudo tee /etc/supervisord.conf > /dev/null

sudo mkdir -p /var/log/ticker
sudo mkdir -p /var/log/supervisord
sudo pip install supervisor

# start supervisord
sudo supervisorctl stop all
sudo killall -9 supervisord
sudo supervisord -c /etc/supervisord.conf
