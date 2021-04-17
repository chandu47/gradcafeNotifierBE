from main import app
from database.db import init_db
from controller.user_controller import user_controller
from user_settings.controller import settings_controller
from controller.utils_controller import utils_controller
from results_reporting.controller import results_controller
from results_reporting.scrap_gc_job import ScrapGCJob
from config import Config, ProductionConfig, DevelopmentConfig
"""
    Configure db string her
"""

def registerBlueprints():
    app.register_blueprint(user_controller)
    app.register_blueprint(settings_controller)
    app.register_blueprint(utils_controller)
    app.register_blueprint(results_controller)



init_db(app)
registerBlueprints()

print("Starting app")
app.run()