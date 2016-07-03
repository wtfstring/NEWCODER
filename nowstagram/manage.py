# -*- encoding=UTF-8 -*-

from nowstagram import app,db
from flask_script import Manager
from nowstagram.models import User,Image,Comment
import random
from sqlalchemy import or_,and_   #用于查询语句中条件的关联

manager = Manager(app)

def get_image_url():
    return 'http://images.nowcoder.com/head/' + str(random.randint(0,1000)) + 'm.png'

@manager.command
def init_database():
    db.drop_all()
    db.create_all()

    # 创建一些用户,写入到数据库中

    for i in range(0,100):
        db.session.add(User('User' + str(i+1),'a' + str(i)))
        for j in range(0,10):  #为每个人创建10张图片,为了演示AJAX(异步加载)，原来是三张
            db.session.add(Image(get_image_url(),i + 1))
            for k in range(0,3): #为图片加三个评论
                db.session.add(Comment('This is a comment ' + str(k),1+3*i+j,i+1))
    db.session.commit()

    #更新操作方法一
    for i in range(50,100,2):
        user = User.query.get(i)
        user.username = '[New]' + user.username
    #更新操作方法二
    User.query.filter_by(id=51).update({'username':'[New2]'})
    db.session.commit()

    #删除操作
    for i in range(50,100,2):
        comment = Comment.query.get(i+1)
        db.session.delete(comment)
    db.session.commit()

    #开始查询
    #一对一的查询
    print 1,User.query.all()
    print 2,User.query.get(3)
    print 3,User.query.filter_by(id=5).first()
    print 4,User.query.order_by(User.id.desc()).offset(1).limit(2).all()
    print 5,User.query.filter(User.username.endswith('0')).limit(3).all()
    print 6,User.query.filter(or_(User.id == 88,User.id == 99)).all()
    print 7,User.query.filter(and_(User.id > 88,User.id < 93)).all()
    print 8, User.query.filter(and_(User.id > 88, User.id < 93)).first_or_404() #表示结果不为空打印第一个，否则返回404
    print 9,User.query.paginate(page=1,per_page=10).items #分页
    print 9, User.query.order_by(User.id.desc()).paginate(page=1, per_page=10).items

    #一对多的查询
    user = User.query.get(1)
    print 10,user.images

    image = Image.query.get(1)
    print 11,image,image.user




if __name__ == '__main__':
    manager.run()