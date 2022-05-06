from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random
from . import db
import json
from .models import User

views = Blueprint('views', __name__)

# Home page


@views.route("/homepage")
@login_required
def homePage():
    return render_template("homepage.html", user=current_user)

# Photos page


@views.route("/photos")
@login_required
def photos():
    photos = ["static/photos/1.jpg", "static/photos/2.jpg", "static/photos/3.jpg",
              "static/photos/4.jpg", "static/photos/5.jpg", "static/photos/6.jpg", "static/photos/7.jpg"]
    return render_template("photos.html", photos=photos , user=current_user)

# User Settings


@views.route("/setting")
@login_required
def userSettings():
    return render_template("usersettings.html" , user=current_user)

# About page

@views.route("/about")
@login_required
def about():
    return render_template("about.html" , user=current_user)


# Contact page

@views.route("/contact")
@login_required
def contact():
    return render_template("contact.html" , user=current_user)
