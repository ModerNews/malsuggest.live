#!/bin/sh
export BANNER=$(ls ../src/static/images/banners | sort -R | tail -1)
echo $BANNER
