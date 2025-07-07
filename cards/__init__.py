from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from instance.config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

# from flask_session import Session

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

mail = Mail(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

from .views import study as main_blueprint
app.register_blueprint(main_blueprint, url_prefix='/study' ) 

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='')

from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')
# from .api import api as program_apis
# app.register_blueprint(program_apis, url_prefix='/apis')

# session =  Session(app)
api = Api(app)

app.app_context().push()

from  cards import views