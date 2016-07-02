# - * -encoding=UTF-8
from flask_script import Manager  #外部脚本控制文件，可以初始化，跑任务
from c2 import app

manager = Manager(app)

@manager.option('-n','--name',dest='name',default='nowcoder')  #定义一个带参数命令
def hello(name):
    print 'hello',name

@manager.command #定义一个命令
def initalize_database():
    'initialize database'
    print 'database...'

if __name__ == '__main__':
    manager.run()