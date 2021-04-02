from app_settings import app
from database.db import init_db
from controller.user_controller import user_controller
from user_settings.controller import settings_controller
from controller.utils_controller import utils_controller

"""
    Configure db string here
"""
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/gc-notifier'
}

def registerBlueprints():
    app.register_blueprint(user_controller)
    app.register_blueprint(settings_controller)
    app.register_blueprint(utils_controller)


init_db(app)
registerBlueprints()
app.run(debug=True)