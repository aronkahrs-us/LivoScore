import requests

class Auth:
    def __init__(self, user, token) -> None:
        self.user = user
        self.token = token
        pass

    def is_authorized(self):
        rq = requests.get(
            "https://campo.pythonanywhere.com/auth",
            params={
                "user": self.user,
                "token": self.token,
            },
        )
        return rq.status_code==200