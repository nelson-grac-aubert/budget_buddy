#  la logique du menu d’acceuil, du login, du register
# hachage mdp
import re
import bcrypt

def validate_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{10,}$'
    return re.match(pattern, password)

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())