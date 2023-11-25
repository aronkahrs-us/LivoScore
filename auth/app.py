from flask import Flask, request
from google.cloud import firestore
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    "auth/livoscore-firebase-adminsdk-25gdu-3974371e33.json"
)
db = firestore.Client(project="livoscore", credentials=credentials)
users = db.collection("Users")

app = Flask(__name__)


@app.route("/auth")
def auth():
    user = request.args.get("user")
    token = request.args.get("token")
    user_docs = users.where(filter=firestore.FieldFilter("ID", "==", user)).stream()
    for user in user_docs:
        if token in user.to_dict().values():
            users.document(user.id).update({"lastConnection": firestore.SERVER_TIMESTAMP})
            return "OK", 200
        else:
            return "NO", 401


if __name__ == "__main__":
    app.run(debug=True)
