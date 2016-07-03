# -*- encoding=UTF-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#ORM 关系对象映射，实质是将关系数据库中的业务数据用对象的形式表示出来，并通过面向对的方式
    #将这些对象组织起来,而SQLAlchemy是流行的ORM框架

app = Flask(__name__)  #创建一个应用
app.jinja_env.add_extension('jinja2.ext.loopcontrols')  #增加对break的支持
app.config.from_pyfile('app.conf')  #从文件初始化一个应用
app.secret_key = 'nowcoder'
db = SQLAlchemy(app)  #db 数据库
login_manager = LoginManager(app)  #用户初始化
login_manager.login_view = '/regloginpage/'  #如果用户没有登录，自定义跳到某个页面，这里跳到注册页面

from nowstagram import views,models



