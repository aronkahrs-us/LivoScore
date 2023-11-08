import threading
from flask import Flask, render_template,request


class Court(threading.Thread):
    def __init__(self,match,  *args, **kwargs):
        super(Court, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.app = Flask(__name__)

        @self.app.route("/")
        def index():
            return render_template(
                "court.html", home=match.home.players, away=match.away.players
            )
    
    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def start(self):
        self._stop_event.clear()
        self.app.run()