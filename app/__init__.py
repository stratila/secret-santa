from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from telebot import TeleBot

telegram_bot = TeleBot(token=Config.BOT_TOKEN)

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models, bot_state, bot_messages
