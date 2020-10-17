from flask import request, redirect, render_template
from flask_login import login_required, login_user, logout_user, current_user

from app import app, db

from .forms import SignupForm, LoginForm, ProfileEditForm
from .models import User


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template("accounts/signup.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        login_user(form.user)
        return redirect("/")
    return render_template("accounts/login.html", form=form)


@login_required
@app.route("/logout")
def logout():
    """Logout."""
    logout_user()
    return redirect("/login")


@app.route("/profile/<username>", methods=['GET', 'POST'])
def profile(username):
    request_username = current_user
    user = User.query.filter_by(username=username).one()

    if request.method == 'POST':
        return redirect(f'/profile/{username}/edit')

    return render_template("accounts/profile.html", user=user, username=request_username)


@app.route("/profile/<username>/edit", methods=['GET', 'POST'])
def profile_edit(username):
    request_username = current_user
    user = User.query.filter_by(username=username).one()
    form = ProfileEditForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            user.username = form.username.data,
            user.email = form.email.data,
            db.session.add(user)
            db.session.commit()
            return redirect(f'/profile/{user.username}')

    return render_template("accounts/profile_edit.html", user=user, form=form, username=request_username)


