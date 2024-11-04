from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer)
    emotions = db.Column(db.JSON)
    risk_assessment = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
