import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    branch = os.environ.get('BRANCH_NAME', 'unknown')
    return f"Hello World from {branch} branch!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
