from passlib.context import CryptContext

pwd_context = CryptContext(["bcrypt"])


def generate_hash(text: str):
    return pwd_context.hash(text)


def verify_hash(text: str, hash_txt: str):
    return pwd_context.verify(text, hash_txt)

