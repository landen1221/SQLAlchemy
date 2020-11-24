"""Blogly application."""

from flask import Flask, request, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users, Post
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    users = Users.query.all()
    return render_template('user-listing.html', users=users)

@app.route('/', methods=["POST"])
def create_user():
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']
    if image_url:
        new_user = Users(first_name=first_name, last_name=last_name, image_url=image_url)
    else:
        new_user = Users(first_name=first_name, last_name=last_name)
    
    db.session.add(new_user)
    db.session.commit()

    return redirect('/')

@app.route('/create-user')
def add_user():
    return render_template('create-user.html')

@app.route('/user-details/<id>')
def details(id):
    user = Users.query.get_or_404(id)
    posts = Post.query.filter(Post.user_id == id)
    print(f'Printing posts: {posts}')
    return render_template('user-details.html', user=user, posts=posts)



@app.route('/user-details/<id>', methods=['POST'])
def add_post_to_user(id):
    title = request.form['post-title']
    content = request.form['post-content']

    post = Post(title=title, content=content, created_at=datetime.datetime.now(), user_id=id)
    db.session.add(post)
    db.session.commit()

    return redirect(f'/user-details/{id}')



@app.route('/edit-user/<user_id>')
def edit(user_id):
    user = Users.query.get(user_id)
    return render_template('edit-user.html', user=user)

@app.route('/edit-user/<user_id>', methods=['POST'])
def updated(user_id):
    user = Users.query.get(user_id)
    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['image-url']

    db.session.add(user)
    db.session.commit()

    return redirect(f'/user-details/{user.id}')

@app.route('/delete-user/<user_id>', methods=['POST'])
def delete_user(user_id):
    print('entered function')
    Users.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/')

@app.route('/add-post/<id>')
def new_post(id):
    user = Users.query.get(id)
    return render_template('add-post.html', user=user)


@app.route('/post-details/<post_id>')
def display_post(post_id):
    post = Post.query.get(post_id)

    return render_template('post-details.html', post=post)

@app.route('/delete-post/<post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    user_id = post.user_id
    
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    
    return redirect(f'/user-details/{user_id}')

@app.route('/edit-post/<id>')
def edit_post(id):
    post = Post.query.get(id)
    return render_template('edit-post.html', post=post)

@app.route('/edit-post/<id>', methods=['POST'])
def edited_post(id):
    post = Post.query.get(id)
    user_id = post.user_id
    post.title = request.form['post-title']
    post.content = request.form['post-content']
    post.created_at = datetime.datetime.now()
    
    db.session.add(post)
    db.session.commit()

    return redirect(f'/user-details/{user_id}')

