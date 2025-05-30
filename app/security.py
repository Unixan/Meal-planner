import bcrypt

ENCODING = "utf-8"

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(ENCODING), salt)
    return hashed.decode(ENCODING)

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(ENCODING), hashed.encode(ENCODING))
