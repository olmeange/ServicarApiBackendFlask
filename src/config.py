from decouple import config

class Config:
    SECRET_KEY=config('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG=True
    HOST='192.168.100.14'
    PORT=5000

config={
    'development': DevelopmentConfig
}    