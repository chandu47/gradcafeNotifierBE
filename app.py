from flask import Flask

app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
    print("Using Production env")
else:
    app.config.from_object("config.DevelopmentConfig")
    print("Using Development env")