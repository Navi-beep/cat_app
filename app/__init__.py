from flask import Flask
from config import Config 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS 



app = Flask(__name__)
CORS(app)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = 'You must be logged in to do stuff like that!!'
login.login_message_category = 'danger'


from . import routes , models 