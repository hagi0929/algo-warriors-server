from bcrypt import hashpw, gensalt, checkpw


def hash_password(password: str) -> str:
    hashed = hashpw(password.encode('utf-8'), gensalt())
    return hashed.decode('utf-8')


def check_password(provided_password: str, stored_password: str) -> bool:
    return checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))
