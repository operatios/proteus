from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hash: str) -> bool:
    # await run_in_threadpool()
    return password_hash.verify(password, hash)


def authenticate(username: str, password: str) -> None:
    # user = UserService(session).get(username)
    # if user:
    # verify_password(password, user.hashed_password)
    # else:
    # verify_password(password, DUMMY_HASH)

    # return user

    return None


DUMMY_HASH = hash_password("hunter2")
