#! /bin/bash
if [ -n "$NET_DELAY" ]; then
    echo "Setting network delay to ${NET_DELAY}ms"
    tc qdisc add dev eth0 root netem delay "${NET_DELAY}"ms
fi
python manage.py runserver 0.0.0.0:8080