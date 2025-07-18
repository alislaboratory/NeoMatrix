#!/bin/bash
export FLASK_APP=app.py
export FLASK_ENV=production
# Listen on all interfaces so you can connect from elsewhere
flask run --host=0.0.0.0
