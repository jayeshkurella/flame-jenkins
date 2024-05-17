call venv/scripts/activate
color 4B
title Flame_With_SSL DEV New  Server

rem To run default django server
rem call python manage.py runserver 0.0.0.0:7002

rem To Run with SSL
call python manage.py runsslserver 0.0.0.0:7002 --certificate "C:\Certbot\live\portal.coderize.in\cert.pem" --key "C:\Certbot\live\portal.coderize.in\privkey.pem"
