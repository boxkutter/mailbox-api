from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()   # flask-sqlalchemy
ma = Marshmallow()  # marshmallow-sqlalchemy

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    db.init_app(app)

    with app.app_context():
        from . import routes  # Import routes
        
        return app



# import os

# from flask import Flask,jsonify
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Column, Integer, String, DateTime

# def create_app(test_config=None):
#     # create and configure the app
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         SECRET_KEY='dev',
#         DATABASE=os.path.join(app.instance_path, 'mailbox.db'),
#         SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'mailbox.db'),
#         SQLALCHEMY_TRACK_MODIFICATIONS=False   
#     )

#     if test_config is None:
#         # load the instance config, if it exists, when not testing
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         # load the test config if passed in
#         app.config.from_mapping(test_config)

#     # ensure the instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass
