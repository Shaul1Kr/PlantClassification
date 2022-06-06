from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from sqlalchemy import null
from .models import User, Photos
from werkzeug.security import generate_password_hash, check_password_hash
import random
from . import db
import json
import pandas as pd
from datetime import date
from PIL import Image
# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

import numpy as np
from util import base64_to_pil

from tensorflow.keras.preprocessing import image
from keras.models import load_model


views = Blueprint('views', __name__)

# Model saved with Keras model.save()
# MODEL_PATH_1 = "website/static/bestmodel_23class.h5"

# Load my own trained model
model_1 = load_model("website/static/bestmodel_23class.h5")

print('Model loaded.. Check http://127.0.0.1:5000/')
print('Model loaded. Start serving...')

# Declare class names for labels
class_dict = {'Beeblossom': 0, 'Begonia Maculata': 1, 'Coleus': 2, 'Crown of thorns': 3, 'Elephant_s Ear': 4, 'House Leek': 5, 'Jade Plant': 6, 'Limonium sinuatum': 7, 'Lucky Bamboo': 8, 'Mesquites': 9, 'Moon Cactus': 10, 'Myoporum': 11,
              'Nerve Plant': 12, 'Paddle Plant': 13, 'Parlor Palm': 14, 'Pennisetum': 15, 'Poinsettia': 16, 'Sansevieria Ballyi': 17, 'String Of Banana': 18, 'Venus Fly Trap': 19, 'Zebra Cactus': 20, 'echeveria': 21, 'woolly senecio': 22}
class_names = list(class_dict.keys())


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
    return render_template("homepage.html", user=current_user)


# Photos page

@views.route("/photos")
@login_required
def photos():
    records = Photos.query.filter_by(userId=current_user.id).all()
    all_photos = []
    for photo_record in records:
        photoPath = 'website/static/photos/' + photo_record.name
        writeTofile(photo_record.photo, photoPath)
        all_photos.append("../static/photos/" + photo_record.name)
    return render_template("photos.html", photos=all_photos, user=current_user)

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

# Pradict page


@views.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the image from post request
        img = base64_to_pil(request.json)

        # Make prediction
        preds1 = model_predict1(img, model_1)
        index_pred1 = np.argmax(preds1)

        # Confidence
        confidence1 = "{}".format(preds1[0][index_pred1])
        index = 0
        result = class_names[index_pred1]
        index = index_pred1
        confidence = float(confidence1)*100

        # Read description from excel file according to the prediction of given image
        data = pd.read_excel(r'./website/descriptions.xlsx')
        df = pd.DataFrame(
            data, columns=['Label', 'Class', 'Scientific_name', 'Watering', 'Sun_Exposure', 'Soil_Type', 'Bloom_Time', 'Pests_Diseases', 'Toxicity'])

        row = df.iloc[index]
        myDes = []
        myDes.append(round(confidence, 2))
        myDes.extend([row[1], row[2], row[3], row[4],
                     row[5], row[6], row[7], row[8]])

        # Return predicted class, confidence and description.
        return jsonify(result=[result, 'Class:\t'+str(myDes[1]), 'Confidence:\t'+str(myDes[0])+'%', 'Scientific name:\t'+str(myDes[2]), 'Watering:\t'+str(myDes[3]), 'Sun Exposure:\t'+str(myDes[4]), 'Soil Type:\t'+str(myDes[5]), 'Bloom Time:\t'+str(myDes[6]), 'Pests & Diseases:\t'+str(myDes[7]), 'Toxicity:\t'+str(myDes[8])])
    return None

# User Management page


@views.route('/userManagement', methods=['GET', 'POST'])
@login_required
def userManagment():
    if current_user.admin == True:
        if request.method == 'POST':
            if request.form.get("editphide") == "1":  # edit a user
                user = User.query.filter_by(
                    id=int(request.form.get("editId"))).first()
                user.email = request.form.get("email")
                user.password = generate_password_hash(
                    request.form.get("password"), method='sha256')
                user.auth = request.form.get("admin")
                db.session.add(user)
                db.session.commit()
            elif request.form.get("deletephide") == "1":  # delete a user
                user = User.query.filter_by(
                    id=int(request.form.get("deleteId"))).first()
                db.session.delete(user)
                db.session.commit()
            users = User.query.all()
            return render_template("userManagment.html", user=current_user, alluser=users)
        users = User.query.all()
        return render_template("userManagment.html", user=current_user, alluser=users)
    else:
        return render_template("homepage.html", user=current_user)


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")


@views.route('/saveImage', methods=['GET', 'POST'])
def saveImage():
    if request.method == 'POST':
        img = request.files
        payload = request.headers
        class_predict = payload['class_description']
        today = date.today()
        print("IASDSADAS", class_predict[7:])
        img1 = Image.open(img.get('files'))
        img1 = img1.save('savedimage.jpg')
        photo = convertToBinaryData('./savedimage.jpg')
        newPhoto = Photos(userId=current_user.id, photo=photo,
                          name=img.get('files').filename, date=today.strftime("%B %d, %Y"), class_predict=class_predict[7:])
        db.session.add(newPhoto)
        db.session.commit()
        return 'Ok'
    return None
