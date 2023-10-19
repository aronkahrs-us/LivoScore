from .apiv3 import Match
from flask import Flask, render_template


class plyrList:
    def __init__(self, match: Match) -> None:
        self.app = Flask(__name__)

        @self.app.route("/")
        def index():
            return render_template(
                "index.html", home=match.home, away=match.away
            )

    def start(self):
        self.app.run()
