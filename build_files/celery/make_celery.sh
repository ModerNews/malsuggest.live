#!/bin/sh
# Remember, systemd is not default on Debian
echo "Creating user and group for celery"
useradd celery

# Create the celeryd config, strip windows signs
mv ./celery_deamon/celeryd /etc/default/celeryd
cp /etc/default/celeryd celeryd
cat celeryd | tr -d '\r' > celeryd
cp celeryd /etc/default/celeryd
chmod 640 /etc/default/celeryd # Write-prevent celeryd config
rm celeryd

# Copy default celeryd init script
touch /etc/init.d/celeryd
wget https://raw.githubusercontent.com/celery/celery/main/extra/generic-init.d/celeryd -O celeryd
cp celeryd /etc/init.d/celeryd

chmod +x /etc/init.d/celeryd

/etc/init.d/celeryd start
