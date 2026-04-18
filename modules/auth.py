from modules.db import get_user, add_user

def signup(username, password):
    if get_user(username):
        return False
    add_user(username, password)
    return True

def login(username, password):
    user = get_user(username)
    if user and user[1] == password:
        return True
    return False