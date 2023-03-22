#!/bin/sh
echo "Creating user and group for celery"
groupadd celery 
useradd celery -G celery 

mv ./build_files/celery.service /etc/systemd/system
mv ./build_files/celery /etc/conf.d
mv ./build_files/celery.conf /etc/tmpfiles.d

systemctl enable celery.service
systemctl start celery.service