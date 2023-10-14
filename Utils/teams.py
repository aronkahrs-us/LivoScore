from apiv3 import Match
from flask import Flask, render_template

class Teams:
    def __init__(self,match) -> None:
        app = Flask(__name__)
        @app.route('/')
        def index():
            return render_template('index.html',home=match.home['Players'],away=match.away['Players'])

        if __name__=='__main__':
            app.run(debug=True)

Teams(Match(5979,'livosur'))