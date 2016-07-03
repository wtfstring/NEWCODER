# -*- encoding=UTF-8 -*-

from nowstagram import db,login_manager
from datetime import datetime
import random

class Comment(db.Model):  #评论类包括评论内容，针对哪个用户的哪个图片，id用于区分内容，每个表都要有id
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.String(1024))
    image_id = db.Column(db.Integer,db.ForeignKey('image.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    status = db.Column(db.Integer,default=0) # 0 正常 1 被删除
    user = db.relationship('User') #将评论和User表关联起来

    def __init__(self,content,image_id,user_id): #构造函数
        self.content = content
        self.image_id = image_id
        self.user_id = user_id

    def __repr__(self):  #此函数实现对类的打印，是默认的函数
        return '<Command %d %s>' % (self.id, self.content)

class Image(db.Model):  #图片类
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    url = db.Column(db.String(512))  #图片的来源
    user_id = db.Column(db.Integer,db.ForeignKey('user.id')) #通过外键建立Image与User之间的关系
    create_date = db.Column(db.DateTime)  #图片的上传时间
    comments = db.relationship('Comment') #将评论和image关联

    def __init__(self,url,user_id):
        self.url = url
        self.user_id = user_id
        self.create_date = datetime.now()  #图片的上传时间为当前的时间，从模块datetime而来

    def __repr__(self):
        return '<Image %d %s>' % (self.id,self.url)

class User(db.Model):  #用户类
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(80),unique=True)
    password = db.Column(db.String (32))
    salt = db.Column(db.String(32))
    head_url = db.Column(db.String(256))
    images = db.relationship('Image',backref='user',lazy='dynamic')  #参数Image表示图片类(表),lazy表示加载时机

    def __init__(self,username,password,salt=''):
        self.username = username
        self.password = password
        self.salt = salt
        self.head_url = 'http://images.nowcoder.com/head/' + str(random.randint(0,1000)) + 'm.png'

    def __repr__(self):
        return '<User %d %s>' %(self.id,self.username)

    @property
    def is_authenticated(self):
        return True;

    @property
    def is_active(self):
        return True;

    @property
    def is_anonymous(self):
        return False;

    def get_id(self):
        return self.id;

#用户加载
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)