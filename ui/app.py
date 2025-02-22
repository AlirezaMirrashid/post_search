
# import os
# from flask import Flask, render_template, request, redirect, url_for
# import requests

# app = Flask(__name__)

# # Service URLs (pointing to the API Gateway)
# API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://api_gateway:3000/")

# @app.route('/')
# def home():
#     # Redirect to create post page as default
#     return redirect(url_for('post'))

# @app.route('/post')
# def post():
#     return render_template("post.html", active_tab="post")

# @app.route('/create_post', methods=['POST'])
# def create_post():
#     content = request.form.get("content")
#     if content:
#         # Send the post creation request to the API Gateway
#         requests.post(f"{API_GATEWAY_URL}create_post", json={"content": content})

#     return redirect(url_for('post'))

# @app.route('/like')
# def like():
#     return render_template("like.html", active_tab="like")

# @app.route('/like_post', methods=['POST'])
# def like_post():
#     post_id = request.form.get("post_id")
#     if post_id:
#         # Send the like request to the API Gateway
#         requests.post(f"{API_GATEWAY_URL}like_post", json={"post_id": post_id})
#     return redirect(url_for('like'))

# @app.route('/search')
# def search():
#     keyword = request.args.get("keyword", "")
#     sort_by = request.args.get("sort_by", "recency")
#     search_type = request.args.get("search_type", "match")
#     posts = None
#     if keyword:
#         # Send the search request to the API Gateway
#         response = requests.get(f"{API_GATEWAY_URL}search", params={
#             "keyword": keyword,
#             "sort_by": sort_by,
#             "search_type": search_type
#         })
#         posts = response.json()
#     return render_template("search.html", active_tab="search", posts=posts)

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

import os
from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Needed for flashing messages

# Service URL (pointing to the API Gateway) without a trailing slash
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://api_gateway:3000/").rstrip("/")

# Define the authorization header (using the dummy token)
AUTH_HEADERS = {"Authorization": "Bearer secret_token"}

@app.route('/')
def home():
    # Redirect to the post creation page by default
    return redirect(url_for('post'))

@app.route('/post')
def post():
    return render_template("post.html", active_tab="post")

@app.route('/create_post', methods=['POST'])
def create_post():
    content = request.form.get("content")
    if content:
        try:
            # Send the post creation request to the API Gateway with the auth header
            response = requests.post(
                f"{API_GATEWAY_URL}/create_post",
                json={"content": content},
                headers=AUTH_HEADERS
            )
            if response.status_code != 200:
                flash("Error creating post.", "error")
        except requests.exceptions.RequestException:
            flash("Error creating post.", "error")
    return redirect(url_for('post'))

@app.route('/like')
def like():
    return render_template("like.html", active_tab="like")

@app.route('/like_post', methods=['POST'])
def like_post():
    post_id = request.form.get("post_id")
    if post_id:
        try:
            # Send the like request to the API Gateway with the auth header
            response = requests.post(
                f"{API_GATEWAY_URL}/like_post",
                json={"post_id": post_id},
                headers=AUTH_HEADERS
            )
            if response.status_code != 200:
                flash("Error liking post.", "error")
        except requests.exceptions.RequestException:
            flash("Error liking post.", "error")
    return redirect(url_for('like'))

@app.route('/search')
def search():
    keyword = request.args.get("keyword", "")
    sort_by = request.args.get("sort_by", "recency")
    search_type = request.args.get("search_type", "match")
    posts = None
    if keyword:
        try:
            # Send the search request to the API Gateway with the auth header
            response = requests.get(
                f"{API_GATEWAY_URL}/search",
                params={
                    "keyword": keyword,
                    "sort_by": sort_by,
                    "search_type": search_type
                },
                headers=AUTH_HEADERS
            )
            if response.status_code == 200:
                posts = response.json()
            else:
                flash("Error performing search.", "error")
        except requests.exceptions.RequestException:
            flash("Error performing search.", "error")
    return render_template("search.html", active_tab="search", posts=posts)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
