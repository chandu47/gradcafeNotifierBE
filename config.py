class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY="i\x83\x8a\xc4J$\xa7>\x0e\xe41Ow\xe0\xc6\x86"
    MONGODB_SETTINGS = { 'host': 'mongodb+srv://admin:mongodb-bom@cluster-bom.9syk2.mongodb.net/gc-notifier?retryWrites=true&w=majority'}


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"
    pass

class ProductionConfig(Config):
    pass
