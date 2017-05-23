# -*- encoding=utf-8 -*-
from lsinstagram import db
import random
from datetime import datetime

class Comment(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    content = db.Column(db.String(1024))
    image_id =  db.Column(db.Integer, db.ForeignKey('image.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Integer,default=0)
    user = db.relationship('User')

    def __init__(self,content,image_id,user_id):
        self.content=content
        self.image_id=image_id
        self.user_id=user_id

    def __repr__(self):
        return '<Comment %d %s>' % (self.id, self.content).encode('gbk')

class Image(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    url = db.Column(db.String(512))
    create_date=db.Column(db.DateTime)
    comments = db.relationship('Comment')

    def __init__(self,url,user_id):
        self.url = url
        self.user_id=user_id
        self.create_date=datetime.now()

    def __repr__(self):
        return '<Image %d %s>' % (self.id, self.username).encode('gbk')

class User(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32))
    salt = db.Column(db.String(32))
    head_url = db.Column(db.String(256))
    images = db.relationship('Image')

    def __init__(self,username,password,salt=''):
       self.username=username
       self.password=password
       self.salt=salt
       head_url='http://images.nowcoder.com/head/'+str(random.randint(0,1000))+'m.png'
    def __repr__(self):
        return ( '<user %d %s>' %(self.id ,self.username )).encode('gbk')