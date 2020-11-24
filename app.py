"""Blogly application."""

from flask import Flask, request, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

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

@app.route('/user-details/<user_id>')
def details(user_id):
    user = Users.query.get_or_404(user_id)
    return render_template('user-details.html', user=user)

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



