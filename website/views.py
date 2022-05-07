from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random
from . import db
import json
from .models import User
# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from util import base64_to_pil


views = Blueprint('views', __name__)

# Model saved with Keras model.save()
MODEL_PATH_1 = 'website/model/bestmodel_23class.hdf5'
# Load my own trained model
model = keras.models.load_model(MODEL_PATH_1)
print('Model loaded.. Check http://127.0.0.1:5000/')
print('Model loaded. Start serving...')

def model_predict1(img, model):
    # Preprocessing the image
    img = img.resize((256, 256))
    x = image.img_to_array(img) / 255
    x = np.expand_dims(x, axis=0)
    preds = model.predict(x)
    return preds

# Home page

@views.route("/homepage")
@login_required
def homePage():
    # Make prediction
    #preds1 = model_predict1(base64_to_pil('website/static/photos/1.jpg'), model)
    #print(preds1)
    return render_template("homepage.html", user=current_user)

# Photos page

@views.route("/photos")
@login_required
def photos():
    photos = ["static/photos/1.jpg", "static/photos/2.jpg", "static/photos/3.jpg",
              "static/photos/4.jpg", "static/photos/5.jpg", "static/photos/6.jpg", "static/photos/7.jpg"]
    
    return render_template("photos.html", photos=photos, user=current_user)

# User Settings


@views.route("/setting")
@login_required
def userSettings():
    return render_template("usersettings.html", user=current_user)

# About page


@views.route("/about")
@login_required
def about():
    return render_template("about.html", user=current_user)

# Contact page


@views.route("/contact")
@login_required
def contact():
    return render_template("contact.html", user=current_user)


