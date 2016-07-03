# -*- encoding=UTF-8 -*-

from nowstagram import app,db
from models import Image,User
from flask import render_template,redirect,request,flash,get_flashed_messages
import random,hashlib,json #给密码加盐,再用MD5方法加密
from flask_login import login_user,logout_user,current_user,login_required

@app.route('/')
def index():
    images = Image.query.order_by('id desc').limit(10).all() #降序排列图片，选出10张图片作为首页的图片
    return render_template('index.html',images=images)  #把图片传进去

@app.route('/image/<int:image_id>/')
def image(image_id):
    image = Image.query.get(image_id)
    if image == None:
        return redirect('/') #跳转到首页index页面
    return render_template('pageDetail.html',image=image)

#用户个人页面
@app.route('/profile/<int:user_id>/')
@login_required  #代表访问此页面需要先登录
def profile(user_id):
    user = User.query.get(user_id)
    if user == None:
        return redirect('/')

    # 演示AJAX(异步加载，不刷新页面，加载数据)查找用户的所有图片,分页，每页三个,没有也不报错
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=1,per_page=3,error_out=False)
    return render_template('profile.html',user=user,images=paginate.items,has_next=paginate.has_next)

#AJAX异步请求接口
@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def user_images(user_id,page,per_page):
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    map ={'has_next':paginate.has_next}
    images = []
    for image in paginate.items:
        imgvo = {'id':image.id,'url':image.url,'comment_count':len(image.comments)}
        images.append(imgvo)
    map['images'] = images
    return json.dumps(map)


#注册登录页面
@app.route('/regloginpage/')
def regloginpage():
    msg = ''
    for m in get_flashed_messages(with_categories=False,category_filter=['reglogin']):
        msg = msg + m
    return render_template('login.html',msg=msg,next=request.values.get('next'))  #登录后通过next回到之前访问的页面


def redirect_with_msg(target,msg,category):
    if msg != None:
        flash(msg,category=category)
    return redirect(target)

#登录页面,登录过程中验证用户名、密码和服务器中的是否一致
@app.route('/login/',methods={'post','get'})
def login():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    if username == '' or password == '':
        return redirect_with_msg('/regloginpage', u'用户名或密码不能为空', 'reglogin')

    user = User.query.filter_by(username=username).first()  #查找该用户是否存在
    if user == None:  #如果用户不存在，即是没有注册过
        return redirect_with_msg('/regloginpage', u'用户名不存在', 'reglogin')

    #如果用户名存在，验证密码
    m = hashlib.md5()
    m.update(password+user.salt)
    if (m.hexdigest() != user.password): #密码不正解
        return redirect_with_msg('/regloginpage', u'密码错误', 'reglogin')

    #密码正确定则登录，并跳转到首页
    login_user(user)

    #next功能的跳转，提升用户体验，返回之间访问的页面
    next = request.values.get('next')
    if next != None and next.startswith('/'):
        return redirect(next)

    return redirect('/')

#注册
@app.route('/reg/',methods={'post','get'})
def reg():
    #request.args
    #request.form
    username = request.values.get('username').strip()  #strip 去除前后空格
    password = request.values.get('password').strip()

    if username == '' or password == '':
        return redirect_with_msg('/regloginpage', u'用户名或密码不能为空', 'reglogin')

    user = User.query.filter_by(username=username).first()
    if user != None:
        return redirect_with_msg('/regloginpage',u'用户名已经存在','reglogin')

    #注册帐号更多判断

    salt = '.'.join(random.sample('0123456789abcdefghiABCDEFGHI',10))
    m = hashlib.md5() #原来的密码
    m.update(password+salt)  #加盐强化后的密码
    password = m.hexdigest()
    user = User(username,password,salt)
    db.session.add(user)
    db.session.commit()

    #注册完自动登录
    login_user(user)

    next = request.values.get('next')
    if next != None and next.startswith('/'):
        return redirect(next)

    return redirect('/')

#登录退出
@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')


