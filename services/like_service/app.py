
import os
from flask import Flask
from routes import like_routes
from database import engine, Base

app = Flask(__name__)
app.register_blueprint(like_routes, url_prefix="/likes")

# Create tables if not present.
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5002)))
