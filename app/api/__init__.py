from flask import Flask
from app.models.dbModel import db
from app.api.routes.upload import upload_bp
from app.api.routes.emotion_detector import emotion_detector_bp
from app.api.routes.evaluate_risk import evaluate_risk_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.config.Config')

    db.init_app(app)

    app.register_blueprint(upload_bp)
    app.register_blueprint(emotion_detector_bp)
    app.register_blueprint(evaluate_risk_bp)

    return app