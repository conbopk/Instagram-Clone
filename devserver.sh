#!/bin/bash
source .venv/bin/activate
export FLASK_APP=run.py
export FLASK_ENV=development
export FLASK_DEBUG=1
export DATABASE_URL=mysql+pymysql://root:@localhost:3306/instagram_db

flask run --host=0.0.0.0 --port=5000

# Or
Python run.py

