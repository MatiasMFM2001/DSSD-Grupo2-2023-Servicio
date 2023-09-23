from passlib.hash import pbkdf2_sha512


def encrypt(plain_text):
    return pbkdf2_sha512.hash(plain_text)


def encrypt_if_present(key, **kwargs):
    if kwargs.get(key) is not None:
        kwargs[key] = encrypt(kwargs[key])
    return kwargs


def verify(plain_text, hashed_text):
    return pbkdf2_sha512.verify(plain_text, hashed_text)
