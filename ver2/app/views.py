from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import SignUpForm, SigninForm
from models import User
from datetime import datetime


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user



@app.route('/')
def home():
  return render_template('home.html')


@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
  form = SignUpForm()
   
  if request.method == 'POST':
      newuser = User(form.firstname.data, form.lastname.data, form.andrewid.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()

      session['andrewid'] = newuser.andrewid
      login_user(newuser, remember=True)
      return redirect(url_for('profile'))
  elif request.method == 'GET':
    return render_template('signup.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.get(form.andrewid.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return render_template('profile.html', user=user)
    return render_template('signin.html', form=form)


@app.route('/profile')
@login_required
def profile():
  if 'andrewid' not in session:
    return redirect(url_for('login'))
  return render_template('profile.html', user=user)

@app.route('/all')
@login_required
def all():
  for user in db.session.query(User).filter_by(firstname):
     print user
  return redirect(url_for('user', firstname=firstname))

@app.route('/user/<andrewid>')
@login_required
def user(andrewid):
    user = User.query.filter_by(andrewid=andrewid).first()
    if user == None:
        flash('User %s not found.' % andrewid)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html',
                           user=user,
                           posts=posts)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("home.html")