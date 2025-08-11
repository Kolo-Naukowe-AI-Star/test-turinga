from flask import Flask

from test_turinga import FrontendServer


app = Flask(__name__)
app.register_blueprint(FrontendServer())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
