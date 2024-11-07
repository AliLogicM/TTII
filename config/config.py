import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/Analytics'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads/'
    FRAMES_FOLDER = 'uploads/frames/'

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if not os.path.exists(FRAMES_FOLDER):
        os.makedirs(FRAMES_FOLDER)