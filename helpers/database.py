import json
import hashlib
from flask_login import UserMixin

with open('data/users.json') as file:
    users = json.load(file)

class User(UserMixin):
    def __init__(self, username: str, password: str = None, email: str = None):
        self.id = username
        self.username = username
        if password:
            self.password_hash = hashlib.sha3_256(password.encode('utf-8')).hexdigest()
        if email:
            self.email = email

    def create(self):
        users.append(dict(username = self.username,
                          password_hash = self.password_hash,
                          email = self.email))
        with open('data/users.json', 'w') as file:
             json.dump(users,file)

    def verify(self):
        for user in users:
            if user['username'] == self.username :
                if user['password_hash'] == self.password_hash:
                    return True
