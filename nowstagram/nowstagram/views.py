# -*- encoding=UTF-8 -*-

from nowstagram import app,db,mail
from models import Image,User,Comment
from flask import render_template,redirect,request,flash,get_flashed_messages,send_from_directory
import random,hashlib,json,uuid,os # 给密码加盐,再用MD5方法加密
from flask_login import login_user,logout_user,current_user,login_required
import string
from flask_mail import Message

from qiniusdk import qiniu_upload_file

# 首页
@app.route('/')
def index():
    images = Image.query.order_by(db.desc(Image.id)).limit(10).all()  # 降序排列图片，选出10张图片作为首页的图片
    paginate = Image.query.order_by(db.desc(Image.id)).paginate(page=1, per_page=5, error_out=False)
    # return render_template('index.html',images=images)  #把图片传进去
    return render_template('index.html', images=paginate.items, has_next=paginate.has_next)  #把图片传进去

# 首页的“更多命令”
@app.route('/index/images/<int:page>/<int:per_page>/')
def index_images(page, per_page):
    paginate = Image.query.order_by(db.desc(Image.id)).paginate(page=page, per_page=per_page, error_out=False)
    json_data = {'well done!':'shabibi','has_next': paginate.has_next}
    images = []
    for image in paginate.items:
        user = User.query.filter_by(id=image.user_id).first()
        comments = Comment.query.filter_by(image_id=image.id).all()
        comment_username = []
        comment_user_id = []
        comment_content = []
        for c in comments:
            comment_username.append(c.user.username)
            comment_user_id.append(c.user_id)
            comment_content.append(c.content)
        imgvo = {'image_id': image.id,
                 'image_url': image.url,
                 'comment_count': len(image.comments),
                 'image_user_name': user.username,
                 'image_user_id': user.id,
                 'image_user_head_url':user.head_url,
                 'comment_username':comment_username,
                 'created_date':str(image.create_date),
                 'comment_user_id':comment_user_id,
                 'comment_content':comment_content
                 }
        images.append(imgvo)

    json_data['images'] = images
    return json.dumps(json_data)

#图片详情页面
@app.route('/image/<int:image_id>/')
@login_required
def image(image_id):
    image = Image.query.get(image_id)
    if image == None:
        return redirect('/') #跳转到首页index页面
    comments = Comment.query.filter_by(image_id=image_id).order_by(db.desc(Comment.id)).limit(20).all()
    return render_template('pageDetail.html',image=image, comments=comments)

#用户个人页面
@app.route('/profile/<int:user_id>/')
@login_required  #代表访问此页面需要先登录
def profile(user_id):
    user = User.query.get(user_id)
    if user == None:
        return redirect('/')

    # 演示AJAX(异步加载，不刷新页面，加载数据)查找用户的所有图片,分页，每页三个,没有也不报错
    paginate = Image.query.filter_by(user_id=user_id).order_by(db.desc(Image.id)).paginate(page=1,per_page=3,error_out=False)
    return render_template('profile.html',user=user,images=paginate.items,has_next=paginate.has_next)

#AJAX异步请求接口，用户个人页面的“更多”的功能
@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def user_images(user_id,page,per_page):
    paginate = Image.query.filter_by(user_id=user_id).order_by(db.desc(Image.id)).paginate(page=page, per_page=per_page, error_out=False)
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
    #使用 render_template() 方法可以渲染模板
    return render_template('login.html',msg=msg,next=request.values.get('next'))  #登录后通过next回到之前访问的页面

# 注册时的错误处理函数
def redirect_with_msg(target,msg,category):
    if msg != None:
        flash(msg,category=category)
    return redirect(target)

# 登录页面,登录过程中验证用户名、密码和服务器中的是否一致
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


#检测字符串中是否包含某字符集合中的字符
def containAny(seq,charset):
    for c in seq:
        if c not in charset:
            return False;
    return True

#注册
@app.route('/reg/',methods={'post','get'})
def reg():
    #request.args
    #request.form
    username = request.values.get('username').strip()  #strip 去除前后空格
    usermail = request.values.get('usermail')
    password = request.values.get('password').strip()

    if username == '' or password == '' or usermail == '':
        return redirect_with_msg('/regloginpage', u'用户名、密码、邮箱不能为空', 'reglogin')

    lengthofusername = len(username)
    if lengthofusername < 5 or lengthofusername > 16: #用户名长度应该大于4
        return redirect_with_msg('/regloginpage',u'用户名长度应该大于4小于16','reglogin')

    str1 = ''
    str1 += string.letters + '_' + string.digits
    if not containAny(username,str1):
        return redirect_with_msg('/regloginpage',u'用户名只能包含字母或者数字或者下划线','reglogin')

    user = User.query.filter_by(username=username).first()
    if user != None:
        return redirect_with_msg('/regloginpage',u'用户名已经存在','reglogin')

    # 邮箱激活
    lengthOfQQ = len(usermail)
    if lengthOfQQ < 6 or lengthOfQQ > 11:
        return redirect_with_msg('/regloginpage', u'请输入6到11位的QQ号', 'reglogin')
    welcome = "Hello " + username
    sender = app.config['FLASKY_MAIL_SENDER']
    msg = Message(welcome,sender = sender,recipients=[usermail+'@qq.com'])
    msg.body = "Dear"
    msg.html = "<b>Congratulation!<br/>You have succeed to register!</b>"
    #print msg
    mail.send(msg)

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

#保存图片在本地,返回上传图片的url
def save_to_local(file,file_name):
    save_dir = app.config['UPLOAD_DIR']
    file.save(os.path.join(save_dir,file_name))
    return '/image/' + file_name

#图片的访问地址
@app.route('/image/<image_name>')
def view_image(image_name):
    #send_from_directory把文件作为二进制流（http协议头中，不同的文件之前通过boundary分开）发送
    return send_from_directory(app.config['UPLOAD_DIR'],image_name)

#图片上传,而图片的限定格式、保存的位置目录等配置文件应该写在配置文件中
@app.route('/upload/',methods={"post"})  #提交一张图片
@login_required
def upload():
    #print request.files
    file = request.files['file']  #得到上传的文件
    #print dir(file)  # dir()函数返回任意对象的属性和方法列表
    #return 'ok'
    file_ext = ''
    if file.filename.find('.') > 0:  #鉴定文件名是否符合要求
        file_ext = file.filename.rsplit('.',1)[1].strip().lower()  #取出后缀名
    if file_ext in app.config['ALLOWED_EXIT']:
        file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext  #上传的文件名
        #url = save_to_local(file,file_name)  #保存到本地
        url = qiniu_upload_file(file,file_name)
        if url != None:  #将图片加入数据库
            db.session.add(Image(url, current_user.id))
            db.session.commit()

    return redirect('/profile/%d' % current_user.id)

#图片详情页的评论
@app.route('/addcomment/',methods={'post'})
def add_comment():
    image_id = int(request.values['image_id'])
    content = request.values['content'].strip()
    comment = Comment(content,image_id,current_user.id)
    db.session.add(comment)
    db.session.commit()
    return json.dumps({"code":0,"id":comment.id,
                       "content":content,
                       "username":comment.user.username,
                       "user_id":comment.user.id})




