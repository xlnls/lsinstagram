# -*- encoding=utf-8 -*-
from lsinstagram import db,login_manager
import random
from datetime import datetime


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # id是数据库中的一列，主键，自增长
    content = db.Column(db.String(1024))  # 内容
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))  # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 外键
    status = db.Column(db.Integer, default=0)  # 0正常，1表示被删除
    user = db.relationship('User')

    def __init__(self, content, image_id, user_id):
        self.content = content
        self.image_id = image_id
        self.user_id = user_id

    def __repr__(self):
        return '<Comment %d %s>' % (self.id, self.content)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # id是数据库中的一列，主键，自增长
    url = db.Column(db.String(512))  # 地址
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DATETIME)
    comments = db.relationship('Comment')

    def __init__(self, url, user_id):
        self.url = url
        self.user_id = user_id
        self.created_date = datetime.now()

    def __repr__(self):
        return '<Image %d %s>' % (self.id, self.url)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # id是数据库中的一列，主键，自增长
    username = db.Column(db.String(80), unique=True)  # 定义为字符串类型，unique保证唯一
    password = db.Column(db.String(32))  # 定义为字符串类型
    head_url = db.Column(db.String(256))  # 头像
    salt = db.Column(db.String(32))
    images = db.relationship('Image',backref = 'user',lazy = 'dynamic')#关联属性


    def __init__(self, username, password,salt=''):
        self.username = username
        self.password = password
        self.salt=salt
        self.head_url = 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png'  # 使用牛客网自带的1000张随机图片

    def __repr__(self):
        return '<User %d %s>' % (self.id, self.username)


    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)