#!/bin/sh
sh ./roll_banner.sh
/etc/init.d/celeryd start
gunicorn 'runner:create_app()' --bind 0.0.0.0:8000