from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Welcome to Abstergo Corp Online Shopping Portal</h1><p>New features are deployed automatically!</p>"

if __name__ == "__main__":
    # The app runs on port 5000 inside the container
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)