@echo off
color 3A
title Flames Without SSL Server

call venv/scripts/activate
python manage.py runserver 0.0.0.0:7002

