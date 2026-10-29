import os     
from datetime import timedelta    #timedelta: tells duration of time like 5min,20min etc

class Config:
    SECRET_KEY =os.getenv("SECRET_KEY")      
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_TOKEN_EXPIRY = timedelta(minutes=30)


    EMAIL_SERVER = "smtp.gmail.com "    
    EMAIL_PORT_NO = 465               
    EMAIL_USERNAME = os.getenv("MAIL_USERNAME")
    EMAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

