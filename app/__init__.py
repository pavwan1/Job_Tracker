from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = None

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'my_key'    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_COOKIE_SAMESITE'] = 'None' 
    app.config['SESSION_COOKIE_SECURE'] = True
    
    db.init_app(app)
    login_manager.init_app(app)
    CORS(app, supports_credentials=True)
    
    from .routes.jobs import jobs as jobs_blueprint
    app.register_blueprint(jobs_blueprint)
    
    from .routes.pages import pages as pages_blueprint
    app.register_blueprint(pages_blueprint)
    
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    
    return app