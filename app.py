"""Blogly application."""

from flask import Flask, request, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users, Post, PostTag, Tag
from functions import add_tags
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
    
    add_and_commit(new_user)
    

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


#Path when adding a new post
@app.route('/user-details/<id>', methods=['POST'])
def add_post_to_user(id):
    title = request.form['post-title']
    content = request.form['post-content']
    created_at = datetime.datetime.now()
    post = Post(title=title, content=content, created_at=created_at, user_id=id)
    
    add_and_commit(post)

    curr_post = Post.query.filter(Post.created_at == created_at)
    
    #Add tags
    all_tags = db.session.query(Tag.tag_name).all()
    all_tags_list = [v for v, in all_tags]
    

    for tag in all_tags_list:
        try:
            new_tag = request.form[tag]
            tag_used = Tag.query.filter(Tag.tag_name == new_tag).all()
            link_tag = PostTag(post_id=curr_post[0].id, tag_id=tag_used[0].id)
            add_and_commit(link_tag)
        except:
            pass

    return redirect(f'/user-details/{id}')

#Path when editing a post
@app.route('/post-details/<id>', methods=['POST'])
def edited_post(id):
    post = Post.query.get_or_404(id)
    post.title = request.form['post-title']
    post.content = request.form['post-content']
    post.created_at = datetime.datetime.now()

    #Erase all current tags associated with this post
    PostTag.query.filter_by(post_id=id).delete()

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    for tag in tag_ids:
        link_tag = PostTag(post_id=id, tag_id=tag)
        add_and_commit(link_tag)

    add_and_commit(post)




    # all_tags = db.session.query(Tag.tag_name).all()
    # all_tags_list = [v for v, in all_tags]


    # for tag in all_tags_list:
    #     try:
    #         new_tag = request.form[tag]
    #         tag_used = Tag.query.filter(Tag.tag_name == new_tag).all()            

    #         link_tag = PostTag(post_id=id, tag_id=tag_used[0].id)

    #         add_and_commit(link_tag)
    #     except:
    #         pass   

    
    return redirect(f'/post-details/{id}')

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

    add_and_commit(user)

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
    tags = Tag.query.all()
    return render_template('add-post.html', user=user, tags=tags)

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
    tags = Tag.query.all()
    selected_tags = post.post_tag

    tag_list = []

    if selected_tags:
        for tag in selected_tags:
            tag_list.append(tag.tag_name)
    
    return render_template('edit-post.html', post=post, id=id, tags=tags, tag_list=tag_list)


@app.route('/post-details/<post_id>')
def display_post(post_id):
    post = Post.query.get(post_id)
    date = str(post.created_at)[:10]
    tags = post.post_tag
    return render_template('post-details.html', post=post, date=date, tags=tags)

@app.route('/create-tag')
def new_tag():
    return render_template('/create-tag.html')

@app.route('/tags')
def get_tag_list():
    tags = Tag.query.all()
    return render_template('/tags.html', tags=tags)

@app.route('/created-tag', methods=['POST'])
def create_new_tag():
    new_tag = request.form['new-tag']
    
    query = Tag.query.filter(Tag.tag_name == new_tag).all()
    
    if not query:
        create_tag = Tag(tag_name=new_tag)
        add_and_commit(create_tag)    

    return redirect('/tags')

@app.route('/post-tags/<tag_name>')
def get_all_posts_w_tag(tag_name):
    curr_tag = Tag.query.filter(Tag.tag_name == tag_name)
    post_lst = curr_tag[0].posts
    return render_template('post-tags.html', curr_tag=curr_tag, tag_name=tag_name, post_lst=post_lst)

def add_and_commit(data):
    db.session.add(data)
    db.session.commit()