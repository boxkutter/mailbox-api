# mailbox-api

Warning. Python beginner project!

Note to self..

# Setup python3 development environment

python -m venv venv 
.\venv\Scripts\activate
python.exe -m pip install --upgrade pip
$env:FLASK_ENV="development"
$env:FLASKAPP="app.py"

# Install required python modules

pip install flask
pip install flask-sqlalchemy
pip install flask-marshmallow
pip install marshmallow-sqlalchemy
pip install python-dotenv
pip install pylint_flask_sqlalchemy

# Setup test database

flask db_create
flask db_test

To remove: db_drop

# Run the app

flask run

And go to http://localhost:5000
