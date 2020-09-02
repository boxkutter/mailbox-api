"""Mailbox API"""
import os
import sys
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask, jsonify
from sqlalchemy import Column, Integer, String, DateTime

#from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)

# app.config.from_pyfile('config.py')

# Set at user login
OID=1
UID=2


# CONFIG

DATABASE='mailbox.db'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY']='super-secret'
#app.config['MAIL_SERVER'] = os.environ['MAILSERVER']
#app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
#app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '0ef6fcb94d5074'
app.config['MAIL_PASSWORD'] = '04247198b0544c'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

db = SQLAlchemy(app)    # flask-sqlalchemy
ma = Marshmallow(app)   # marshmallow-sqlalchemy
#jwt = JWTManager(app)   # jwt authentication token
#mail = Mail(app)        # for sending email



# Initialize database

@app.cli.command('db_create')
def db_create():
    """Some info"""
    db.create_all()
    print('Database created')


# Delete the database

@app.cli.command('db_drop')
def db_drop():
    """Some info"""
    db.drop_all()
    print('Database dropped')


# Seed the database with test values

@app.cli.command('db_test')
def db_test():
    """Some info"""
    org1 = Organization(name = "Yella Org Ltd.",
                       url = 'http://www.yella.com'
                      )

    org2 = Organization(name = "Big Ltd.",
                       url = 'http://www.big.com'
                      )

    user1 = User(oid=1,
                first_name = "John",
                last_name = "Smith",
                email = "smith@gmail.com",
                password = "qwerty123"
               )

    user2 = User(oid=1,
                first_name = "Ellie",
                last_name = "Blue",
                email = "ellie@gmail.com",
                password = "123abC"
               )

    user3 = User(oid=2,
                first_name = "Bill",
                last_name = "Eon",
                email = "eon@gmail.com",
                password = "qweasd"
               )

    board1 = Board(subject = "My Message Board",
                  uid = 1,
                  created = datetime.strptime("2017-09-05 09:45:28", '%Y-%m-%d %H:%M:%S')
                  )

    board2 = Board(subject = "Another Board",
                  uid = 1,
                  created = datetime.strptime("2017-05-15 09:45:28", '%Y-%m-%d %H:%M:%S')
                  )

    subscriber1 = Subscriber(bid = 1,
                        uid = 1,
                  )
    
    subscriber2 = Subscriber(bid = 1,
                        uid = 2,
                  )

    subscriber3 = Subscriber(bid = 2,
                        uid = 2,
                  )

    subscriber4 = Subscriber(bid = 2,
                        uid = 3,
                  )

    message1 = Message(bid = 1,
                      uid = 1,
                      message = "Hey",
                      created = datetime.strptime("2017-09-05 09:45:00", '%Y-%m-%d %H:%M:%S')
                     )

    message2 = Message(bid = 1,
                      uid = 2,
                      message = "What's up?",
                      created = datetime.strptime("2017-09-05 09:46:00", '%Y-%m-%d %H:%M:%S')
                     )

    message3 = Message(bid = 1,
                      uid = 1,
                      message = "Just testing",
                      created = datetime.strptime("2017-09-05 10:45:00", '%Y-%m-%d %H:%M:%S')
                     )

    message4 = Message(bid = 1,
                      uid = 2,
                      message = "Seems to be working!",
                      created = datetime.strptime("2017-09-05 11:40:00", '%Y-%m-%d %H:%M:%S')
                     )

    message5 = Message(bid = 2,
                      uid = 1,
                      message = "What's this one about?",
                      created = datetime.strptime("2018-09-05 11:40:00", '%Y-%m-%d %H:%M:%S')
                     )

    message6 = Message(bid = 2,
                      uid = 2,
                      message = "I like it!",
                      created = datetime.strptime("2018-09-06 11:40:00", '%Y-%m-%d %H:%M:%S')
                     )

    attachment = Attachment(mid = 1,
                            kb = 256,
                            link = 'https://www.google.com/download.zip',
                            file_hash = 'dirmgn67gkjefd0'
                           )

    timeline = Timeline(mid = 1,
                        added = datetime.strptime("2017-09-05 09:45:29", '%Y-%m-%d %H:%M:%S'),
                        first_viewed = None,
                        last_viewed = None,
                        deleted = None
                       )


    db.session.add(org1)
    db.session.add(org2)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(board1)
    db.session.add(board2)
    db.session.add(subscriber1)
    db.session.add(subscriber2)
    db.session.add(subscriber3)
    db.session.add(subscriber4)
    db.session.add(message1)
    db.session.add(message2)
    db.session.add(message3)
    db.session.add(message4)
    db.session.add(message5)
    db.session.add(message6)
    db.session.add(attachment)
    db.session.add(timeline)

    db.session.commit()
    print('Test data added')



# URL ROUTES

@app.route("/")
def home():
    """Default info"""
    return {
        "App": "mailbox-api",
        "API": "1",
        "Git": "https://github.com/boxkutter/mailbox-api",
    }

@app.route("/info")
def info():
    """Default info"""
    return {
        "App": "mailbox-api",
        "API version": "1",
        "Git": "https://github.com/boxkutter/mailbox-api",
    }




# Admin functions

@app.route('/organizations', methods=['GET'])
def organizations():
    """List all organizations"""
    organizations_list = Organization.query.all()
    result = organizations_schema.dump(organizations_list)
    return jsonify(result)


@app.route('/organization/<int:oid>')
def organization_detail(oid: int):
    """Get organization details"""
    org = Organization.query.filter_by(oid=oid).first()
    if org:
        result = organization_schema.dump(org)
        return jsonify(result)
    else:
        return jsonify(message="That organization doesn't exist"), 401


@app.route('/users', methods=['GET'])
def users():
    """List all users"""
    users_list = User.query.filter_by(oid=OID).order_by('last_name')
    result = users_schema.dump(users_list)
    return jsonify(result)


@app.route('/user/<int:uid>')
def user_detail(uid: int):
    """Get user details"""
    usr = User.query.filter_by(oid=OID,uid=uid).first()
    if usr:
        result = user_schema.dump(usr)
        return jsonify(result)
    else:
        return jsonify(message="That user doesn't exist"), 401


@app.route('/subscribers', methods=['GET'])
def subscribers():
    """List all subscribers"""
    subscribers_list = Subscriber.query.order_by('sid')
    result = subscribers_schema.dump(subscribers_list)
    return jsonify(result)


# User functions

@app.route('/message-board')
def message_board():
    """List all the messages on boards Im subscribed to"""
  
    subscriptions = []
    for subscription in db.session.query(Subscriber).filter_by(uid=UID):
        board = db.session.query(Board).filter_by(bid=subscription.bid).first()

        messages = []
        for message in db.session.query(Message).filter_by(bid=board.bid):
            msg = {
                "mid": message.mid,
                "uid": message.uid,
                "message": message.message 
            }
            messages.append(msg)

        subscribed = { 
            "bid": board.bid, 
            "subject": board.subject, 
            "uid": board.uid,
            "messages": messages
        }
        subscriptions.append(subscribed)
        
    return jsonify(subscriptions)

  


@app.route('/boards')
def boards():
    """List my message boards"""
    boards_list = Board.query.order_by('created').all()
    result = boards_schema.dump(boards_list)
    return jsonify(result)


@app.route('/board/<int:bid>')
def board_content(bid: int):
    """Get board content"""
    brd = Board.query.filter_by(bid=bid).first()
    if brd:
        result = board_schema.dump(brd)
        return jsonify(result)
    else:
        return jsonify(message="That board doesn't exist"), 401


@app.route('/messages')
def messages():
    """List my messages"""
    messages_list = Message.query.order_by('created').all()
    result = messages_schema.dump(messages_list)
    return jsonify(result)


@app.route('/message/<int:mid>')
def message_content(mid: int):
    """Get message content"""
    msg = Message.query.filter_by(mid=mid).first()
    if msg:
        result = message_schema.dump(msg)
        return jsonify(result)
    else:
        return jsonify(message="That message doesn't exist"), 401








# @app.route('/param')
# def param():
#     name = request.args.get('name')
#     age = int(request.args.get('age'))
#     if age < 18:
#         return jsonify(message="Under age"), 404
#     else:
#         return jsonify(message="Welcome " + name)

# @app.route('/params/<string:name>/<int:age>')
# def params(name: str, age: int):
#     if age < 18:
#         return jsonify(message="Under age"), 404
#     else:
#         return jsonify(message="Welcome " + name)




# @app.route('/register', methods=['POST'])
# def register():
#     email = request.form['email']
#     test = User.query.filter_by(email=email).first()
#     if test:
#         return jsonify(message='That user already exists'), 409
#     else:
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
#         password = request.form['password']
#         user = User(first_name=first_name, last_name=last_name, email=email, password=password)
#         db.session.add(user)
#         db.session.commit()
#         return jsonify(message='User created succesfully'), 201



# @app.route('/login', methods=['POST'])
# def login():
#     if request.is_json:
#         email = request.json['email']
#         password = request.json['password']
#     else:
#         email = request.form['email']
#         password = request.form['password']

#     test = User.query.filter_by(email=email, password=password).first()
#     if test:
#         access_token = create_access_token(identity=email)
#         return jsonify(message='Login succeeded', access_token=access_token)
#     else:
#         return jsonify(message='Bas email or password'), 401


# @app.route('/retrieve_password/<string:email>', methods=['GET'])
# def retrieve_password(email: str):
#     user = User.query.filter_by(email=email).first()
#     if user:
#         msg = Message('Your planatary password is ' + user.password,
#                             sender="admin@planets.net",
#                             recipients=[email])
#         mail.send(msg)
#         return jsonify(message="Password sent to " + user.email)
#     else:
#         return jsonify(message="That email doesn't exist"), 401


# @app.route('/planet_details/<int:planet_id>', methods=['GET'])
# def planet_details(planet_id: int):
#     planet = Planet.query.filter_by(planet_id=planet_id).first()
#     if(planet):
#         result = planet_schema.dump(planet)
#         return jsonify(result)
#     else:
#         return jsonify(message="The planet does not exist"), 404

# @app.route('/add_planet', methods=['POST'])
# @jwt_required
# def add_planet():
#     planet_name = request.form['planet_name']
#     test = Planet.query.filter_by(planet_name=planet_name).first()
#     if test:
#         return jsonify(message="The planet already exists"), 409
#     else:
#         planet_type = request.form['planet_type']
#         home_star = request.form['home_star']
#         mass = float(request.form['mass'])
#         radius = float(request.form['radius'])
#         distance = float(request.form['distance'])

#         new_planet = Planet(planet_name=planet_name,
#                             planet_type=planet_type,
#                             home_star=home_star,
#                             mass=mass,
#                             radius=radius,
#                             distance=distance)

#         db.session.add(new_planet)
#         db.session.commit()
#         return jsonify(message="You added a planet"), 201


# @app.route('/update_planet', methods=['PUT'])
# @jwt_required
# def update_planet():
#     planet_id = int(request.form['planet_id'])
#     planet = Planet.query.filter_by(planet_id=planet_id).first()
#     if planet:
#         planet.planet_name = request.form['planet_name']
#         planet.planet_type = request.form['planet_type']
#         planet.home_star = request.form['home_star']
#         planet.mass = float(request.form['mass'])
#         planet.radius = float(request.form['radius'])
#         planet.distance = float(request.form['distance'])
#         db.session.commit()
#         return jsonify(message="Planet updated"), 202

#     else:
#         return jsonify(message="Planet doesn't exist"), 404

# @app.route('/delete_planet/<int:planet_id>', methods=['DELETE'])
# @jwt_required
# def delete_planet(planet_id: int):
#     planet = Planet.query.filter_by(planet_id=planet_id).first()
#     if planet:
#         db.session.delete(planet)
#         db.session.commit()
#         return jsonify(message="You deleted the planet"), 202
#     else:
#         return jsonify(message="Planet not deleted"), 404






# DATA

class Organization(db.Model):
    """Some info"""
    __tablename__ = 'organizations'
    oid = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    url = Column(String, nullable=True)

    # def __init__(self, name):
    #     self.name = name

    def serialize(self):
        return {"id": self.oid,
                "name": self.name,
                "url": self.url}


class User(db.Model):
    """Some info"""
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    oid = Column(Integer)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True)
    password = Column(String)


class Board(db.Model):
    """Some info"""
    __tablename__ = 'boards'
    bid = Column(Integer, primary_key=True)
    subject = Column(String)
    uid = Column(Integer) # owner
    created = Column(DateTime)

class Subscriber(db.Model):
    """Links users to message boards"""
    __tablename__ = 'subscribers'
    sid = Column(Integer, primary_key=True)
    bid = Column(Integer) # board
    uid = Column(Integer) # subscriber


class Message(db.Model):
    """Some info"""
    __tablename__ = 'messages'
    mid = Column(Integer, primary_key=True)
    bid = Column(Integer) # board
    uid = Column(Integer) # author
    message = Column(String)
    created = Column(DateTime)


class Attachment(db.Model):
    """Some info"""
    __tablename__ = 'attachments'
    aid = Column(Integer, primary_key=True)
    mid = Column(Integer)
    kb = Column(Integer)
    link = Column(String)
    file_hash = Column(String)


class Timeline(db.Model):
    """Some info"""
    __tablename__ = 'timeline'
    tid = Column(Integer, primary_key=True)
    mid = Column(Integer)
    added = Column(DateTime)
    first_viewed = Column(DateTime, nullable=True)
    last_viewed = Column(DateTime, nullable=True)
    deleted = Column(DateTime, nullable=True)





# DATABASE SCHEMAS

class OrganizationSchema(ma.Schema):
    """Some info"""
    class Meta:
        """Some info"""
        fields = ('oid','name','url')

organization_schema = OrganizationSchema()
organizations_schema = OrganizationSchema(many=True)

class UserSchema(ma.Schema):
    """Some info"""
    class Meta:
        """Some info"""
        fields = ('oid','uid','first_name','last_name','email','password')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class BoardSchema(ma.Schema):
    """Some info"""
    class Meta:
        """Some info"""
        fields = ('bid','subject','uid','created')

board_schema = BoardSchema()
boards_schema = BoardSchema(many=True)


class SubscriberSchema(ma.Schema):
    """Some info"""
    class Meta:
        """Some info"""
        fields = ('sid','bid')

subscriber_schema = SubscriberSchema()
subscribers_schema = SubscriberSchema(many=True)


class MessageSchema(ma.Schema):
    """Some info"""
    class Meta:
        """Some info"""
        fields = ('mid','bid','uid','message','created')

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)


class AttachmentSchema(ma.Schema):
    """Some info"""
    class Meta:
        """Some info"""
        fields = ('aid','mid','kb','link','file_hash')

attachment_schema = AttachmentSchema()
attachments_schema = AttachmentSchema(many=True)


class TimelineSchema(ma.Schema):
    """Some info"""
    class Meta:
        """Some info"""
        fields = ('mid','added','first_viewed','last_viewed','deleted')

timeline_schema = AttachmentSchema()



if __name__ == '__main__':
    app.run()
