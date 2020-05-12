from flask import *
from flask_pymongo import *
from flask_mail import *
from flask_bcrypt import *
from datetime import *
from PIL import Image
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
import pandas as pd
import os
import uuid
import qrcode


app = Flask(__name__)
app.secret_key = "vc0d373ch345"

app.config["MONGO_URI"] = "mongodb://localhost:27017/eventwk"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

#Upload File Settings
UPLOAD_FOLDER = './static/img'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from main import *




if __name__ == '__main__':
    app.run(debug=True)