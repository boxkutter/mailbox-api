# mailbox-api

Warning. Python beginner project!

Note to self..

## Setup python3 development environment

python -m venv venv  
.\venv\Scripts\activate  
python.exe -m pip install --upgrade pip  
$env:FLASK_ENV="development"  
$env:FLASKAPP="app.py"  

## Install required python modules

pip install flask  
pip install flask-sqlalchemy  
pip install flask-marshmallow  
pip install marshmallow-sqlalchemy  
pip install python-dotenv  
pip install pylint_flask_sqlalchemy  

## Setup test database

flask db_create  
flask db_test  

To remove: db_drop  

## Run the app

flask run  

And go to http://localhost:5000  

## Usage


/mailbox/ - Lists all mailbox topics [GET]  
/mailbox/<topic_id>/ - List all message in a topic [GET]  
/mailbox/<topic_id>/<message_id>/ - Read a single message [GET]  

/mailbox/create-topic [POST] fields: subject  
/mailbox/delete-topic [DELETE]  
/mailbox/create-message [POST] fields: subject-id  
/mailbox/delete-message [DELETE]  





This API uses POST request to communicate and HTTP response codes to indenticate status and errors. All responses come in standard JSON. All requests must include a content-type of application/json and the body must be valid JSON.

###Response Codes

200: Success\
400: Bad request\
401: Unauthorized\
404: Cannot be found\
405: Method not allowed\
422: Unprocessable Entity\
50X: Server Error\
Error Codes Details\
100: Bad Request\
110: Unauthorized\
120: User Authenticaion Invalid\
130: Parameter Error\
140: Item Missing\
150: Conflict\
160: Server Error

###Example Error Message
http code 402\
{\
    "code": 120,\
    "message": "invalid crendetials",\
    "resolve": "The username or password is not correct."\
}\

###Login\
You send: Your login credentials. You get: An API-Token with wich you can make further actions.

Request:

POST /login HTTP/1.1\
Accept: application/json\
Content-Type: application/json\
Content-Length: xy

{\
    "username": "foo",\
    "password": "1234567" \
}\

###Successful Response:

HTTP/1.1 200 OK\
Server: My RESTful API\
Content-Type: application/json\
Content-Length: xy

{\
   "apitoken": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",\
   "expirationDate": "2018-02-13T15:31:55.559Z"\
}

###Failed Response:

HTTP/1.1 401 Unauthorized\
Server: My RESTful API\
Content-Type: application/json\
Content-Length: xy

{\
    "code": 120,\
    "message": "invalid crendetials",\
    "resolve": "The username or password is not correct."\
}



