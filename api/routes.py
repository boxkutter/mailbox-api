"""Application routes."""
from datetime import datetime
from flask import jsonify, current_app as app
from .models import Organization, User, Board, Subscriber, Message, Attachment, Timeline, organizations_schema, organization_schema, users_schema, user_schema, message_schema, messages_schema, board_schema, boards_schema,subscribers_schema

OID=1
UID=1

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
        "App": "my mailbox-api",
        "API": "2",
        "Git": "https://github.com/boxkutter/mailbox-apix",
    }

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
