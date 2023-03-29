#!/bin/sh
# Remember, systemd is not default on Debian
echo "Creating user and group for celery"
useradd celery

chown -R celery:celery /var/log/celery /var/run/celery

# Create the celeryd config, strip windows signs
mv /home/anime_suggester/celery_daemon/celeryd /etc/default/celeryd
# This may be needed if celeryd was modified on windows machine
#cp /.etc/default/celeryd celeryd
#cat celeryd | tr -d '\r' > celeryd
#cp celeryd /etc/default/celeryd
chmod 640 /etc/default/celeryd # Write-prevent celeryd config

# Get default celeryd init script from github
if [[ ! -d '/etc/init.d/' ]]; then
  echo "There is no init.d directory, creating"
  mkdir /etc/init.d/ # Create init.d directory if not existent
fi
touch /etc/init.d/celeryd
wget https://raw.githubusercontent.com/celery/celery/main/extra/generic-init.d/celeryd -O celeryd
cp celeryd /etc/init.d/celeryd

# Uncomment to enable flower interface
#cp ./celery_deamon/flowerd /etc/init.d/flowerd
# chmod +x /etc/init.d/flowerd

chmod 755 /etc/init.d/celeryd
chown root:root /etc/init.d/celeryd
