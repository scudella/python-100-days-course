from flask import Flask, render_template
import requests


app = Flask(__name__)

@app.route('/')
def home():
    blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
    response = requests.get(blog_url)
    posts = response.json()
    return render_template("index.html", posts=posts)

@app.route('/post/<post_id>')
def post(post_id):
    blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
    response = requests.get(blog_url)
    posts = response.json()
    render_post = {}
    for single_post in posts:
        if single_post["id"] == int(post_id):
            render_post = single_post
    return render_template("post.html", post=render_post)

if __name__ == "__main__":
    app.run(debug=True)
