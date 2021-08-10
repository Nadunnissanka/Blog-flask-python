from flask import Flask, render_template
from posts import Post
import requests

BLOG_API_ENDPOINT = 'https://api.npoint.io/c02e0e198d92c805a4c8'

post_list = []
blog_response = requests.get(url=BLOG_API_ENDPOINT).json()
for post in blog_response:
    post_obj = Post(post['id'], post['title'], post['subtitle'], post['author'], post['image'], post['body'])
    post_list.append(post_obj)


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', all_posts=post_list)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/post')
def get_post():
    return render_template('post.html')


if __name__ == "__main__":
    app.run(debug=True)
