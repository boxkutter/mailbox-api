"""Data models."""
from . import db, ma
from flask import current_app as app
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime






# Data

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






# Class functions

class Inbox:

    def __init__(self, uid):
      self.uid = uid

    def list(self):
        subscriptions = []
        
        s = Subscriber.query.filter_by(uid=self.uid).all()

        for x in s: # loop my subscriptions

            board = Board.query.filter_by(bid=x.bid).first()

            messages = []
        
            m = Message.query.filter_by(bid=x.bid).all()

            for y  in m:
                msg = {
                    "mid": y.mid,
                    "uid": y.uid,
                    "messages": y.message
                }
                messages.append(msg)
                
            sub = {
                "bid": board.bid,
                "subject": board.subject,
                "message": messages
            }
            subscriptions.append(sub)

        return subscriptions

    def topic(self):
        return []

    def message(self):
        return []

