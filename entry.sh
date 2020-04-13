#!/bin/sh

if [[ $1 = "dev" ]]; then
    source dev_env
else
    source prod_env
fi
/usr/bin/supervisord -c /etc/supervisord/conf.d/supervisord.conf
