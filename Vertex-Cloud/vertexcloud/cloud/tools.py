import random
import string


files = {
        "document":[".txt", ".pdf",".doc"],
        "photo":[".png",".jpg",".webp"],
        "video":[".mp4", ".3gp"],
        "others":[".html", ".css", ".js"]
        }


def get_ext(filename):
    for types, exts in files.items():
        for ext in exts:
            if filename.endswith(ext):
                return {"type":types,"extension":ext}
    return {"error":"Invalid Filename", "filename":filename}


def session_key_generator(username):
    alpha = string.ascii_lowercase
    key = random.randint(111111,999999)
    user = username[:3] if len(username)>3 else username[::3]
    strings = "".join((random.choice(alpha) for _ in range(4)))

    final_key = f"{strings}{key}{user}"
    return {"user":username, "generated_key":final_key}

class Hasher:
    def hash(self, password):
        hashed = ""

        alpha = string.ascii_lowercase
        beta = string.ascii_uppercase
        gamma = string.digits
        ray = string.punctuation

        keys = {
                alpha : """
                /\
                | |
                | |
                | |
                """,
                beta :"""
                --------->>>>

                ....>>>>


                !!!!
                """,
                gamma : """
                ][[[[----]]]][
                <<<<<>>>>>>>>>
                {->-<->-<->-<->}
                """,
                ray: "1\2\3|6=|"
                }

        temp = []

        for key, value in keys.items():
            for p in password:
                if p in key:
                    temp.append(value)

        hashed = "".join((p for p in temp))
        return {"hashed_password":hashed}


