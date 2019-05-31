# authentication.py

import bcrypt
from database import Database
import datetime

def create_new_user(email, password):

    """
    Attempts to create a new user. Checks for uniqueness on email column. If email already exists, INSERT statement will be ignored

    Args:
        email (string): Email address of user
        password (string): Raw password of user. Password will be encrypted here

    Returns:
        status (string): Status will either be 'success' or 'this user is already registered'
    """

    db = Database()
    status = ''
    insertStatement = "INSERT INTO pfmdatabase.users (email, password, registered_on) VALUES(%s, %s, %s)"
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode('utf-8'), salt)
    now = datetime.datetime.now()

    try:
        db.cur.execute(insertStatement, (email, password, now))
        status = 'success'
        db.conn.commit()
    except:
        status = 'this user is already registered'
    print(status)
    db.conn.close()
    return status

def get_user(email):
    """
    Retrieves user based on email address

    Args:
        email (string): Email address of user
    
    Returns:
        user (dict): Dictionary of user details. Includes:
            - id: id of user
            - email: email of user
            - password: Hashed password of user
            - registered_on: Datetime of when user was registered
            - admin: 1 if user is admin
    """

    db = Database()
    queryStatement = "SELECT * FROM pfmdatabase.users WHERE email = %s"
    db.cur.execute(queryStatement, (email))
    result = db.cur.fetchone()
    user = result
    db.conn.close()

    return user

def login(email, password):
    user = get_user(email)
    hashed_password = user.get('password')

    # bcrypt requires strings to be encoded before checking
    password = password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')

    status = False
    status = bcrypt.checkpw(password, hashed_password)
    
    return status
