#!/bin/bash

# Once this is complete, launch gunicorn
gunicorn -b 0.0.0.0:8003 -w 3 acmi.wsgi:application