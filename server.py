from flask import Flask, render_template, request
from posts import Post
import requests
import smtplib

BLOG_API_ENDPOINT = 'https://api.npoint.io/c02e0e198d92c805a4c8'
MY_EMAIL = "nadunnissankatest@gmail.com"
MY_PASSWORD = "nadun123"
RECEIVE_ADDRESS = "nadunnissanka@yahoo.com"

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


@app.route('/contact')  # methods used to get data & post data
def contact():
    return render_template('contact.html')


@app.route('/post/<int:index>')
def get_post(index):
    selected_post = None
    for single_post in post_list:
        if single_post.post_id == index:
            selected_post = single_post
    return render_template('post.html', current_post=selected_post)


@app.route("/form-entry", methods=["POST", "GET"])
def receive_data():
    data = request.form
    sender_name = data["sendername"]
    sender_email = data["senderemail"]
    sender_phone = data["senderphone"]
    sender_msg = data["sendermsg"]

    # email
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=RECEIVE_ADDRESS,
            msg=f"New Message from {sender_name}\n\nName: {sender_name}\nEmail: {sender_email}\nPhone: {sender_phone}\nMessage: {sender_msg}"
        )
    return render_template('successful.html')


if __name__ == "__main__":
    app.run(debug=True)
