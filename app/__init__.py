from flask import Flask, render_template, redirect, request
from .forms import Form, Login, Blog1, CommentForm, Update, ChangeForm, DeleteComment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required, current_user
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '12342'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
app.app_context().push()

login.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


class Blog3(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    image = db.Column(db.String)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), default=1)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    post = db.Column(db.Integer, db.ForeignKey('blog3.id'))


@login.user_loader
def user_loader(id):
    return User.query.get(int(id))


@app.route('/')
@login_required
def home():
    a = Blog3.query.all()
    return render_template('home.html', a=a, title='Home')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = Form()
    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data
        email = form.email.data
        user = User(username=name, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('registration.html', form=form, title='Registration')


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    form = Blog1()
    file = ''
    if request.method == 'POST':
        file = request.files['image']
        file.save(f'app/static/image/{file.filename}')
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        user = Blog3(title=title, body=body, image=f'app/static/image/{file.filename}')
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('blog.html', form=form, title='Blog')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is None or user.password != password:
            return redirect('/login')
        login_user(user, remember=form.remember.data)
        return redirect('/')
    return render_template('login.html', form=form, title='Login')


@app.route('/change', methods=['GET', 'POST'])
def change():
    form = ChangeForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.commit()
        return redirect('/')
    return render_template('change.html', form=form)


@app.route('/post/<int:id>', methods=['POST', 'GET'])
def post(id):
    post = Blog3.query.get(id)
    comments = Comment.query.filter_by(post=id)
    form = CommentForm()
    if form.validate_on_submit():
        text = form.text.data
        comment = Comment(body=text, user=current_user.id, post=post.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(f'/post/{id}')
    c = []
    for i in comments:
        c.append([i, User.query.get(i.user).username])
    # now = datetime.datetime.now()
    # a = now.strftime('%Y.%m.%d %H %M %S')
    return render_template('post.html', post=post, form=form, comments=comments)


@app.route('/del_post/<int:id>')
def post_del(id):
    post = Blog3.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    post = Blog3.query.get(id)
    form = Update()
    if request.method == 'POST':
        file = request.files['image']
        file.save(f'{post.image}')
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        post.title = title
        post.body = body
        db.session.commit()
        return redirect('/')
    return render_template('update.html', form=form, post=post, title='Update')
