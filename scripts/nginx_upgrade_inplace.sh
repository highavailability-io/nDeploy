#!/bin/bash
kill -s USR2 $(cat /var/run/nginx.pid)
kill -s WINCH $(cat /var/run/nginx.pid.oldbin)
kill -s QUIT $(cat /var/run/nginx.pid.oldbin)
kill -s HUP $(cat /var/run/nginx.pid)
