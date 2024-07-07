import bcrypt
import jwt
from src import jwt


def ecode_string(pwd: str) -> bytes:
    return bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())


def check_pwd(pwd: str, hashed_pwd: bytes) -> bool:
    return bcrypt.checkpw(bcrypt.checkpw(pwd.encode("utf-8"), hashed_pwd))
