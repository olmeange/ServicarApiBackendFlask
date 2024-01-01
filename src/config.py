from decouple import config

class Config:
    SECRET_KEY=config('SECRET_KEY')

    # server folder to save uploaded images and videos
    UPLOAD_FOLDER_IMG = '..\\uploads\\images'
    UPLOAD_FOLDER_VID = '..\\uploads\\videos'
    UPLOAD_FOLDER_DOC = '..\\uploads\\documents'
    UPLOAD_FOLDER_THUMBNAIL = '..\\uploads\\thumbnails'

class DevelopmentConfig(Config):
    DEBUG=True
    HOST='192.168.100.14'
    PORT=5000

config={
    'development': DevelopmentConfig
}    