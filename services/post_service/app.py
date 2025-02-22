

import os
from flask import Flask
from routes import post_routes
from database import engine, Base

app = Flask(__name__)
app.register_blueprint(post_routes, url_prefix="/posts")

# Create database tables if they don't exist.
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5001)))
