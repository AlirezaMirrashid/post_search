
import os
from flask import Flask
from routes import search_routes

app = Flask(__name__)
app.register_blueprint(search_routes, url_prefix="/search")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5003)))
