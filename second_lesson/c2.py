# - * -encoding=UTF-8

from flask import Flask,render_template,request,make_response,redirect,flash,get_flashed_messages
#render_template方法用于关联模板类文件
import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)  #定义一个应用
app.jinja_env.line_statement_prefix = '#'  #指示用作开头
app.secret_key = 'nowcoder'  #运用redirect()两个网页之间跳转，需要key

@app.route('/index/')
@app.route('/')  #路径映射
def index():  #后台处理
    res = ''
    for msg,category in get_flashed_messages(with_categories=True): #从消息队列取出消息
        res = res + category + msg + '<br/>'
    res += 'hello'
    return res

@app.route('/profile/<int:uid>/',methods=['GET','post'])  #<int:uid>表示传入的参数是int,最后的'/'是自动补齐功能，
def profile(uid):
    #return 'profile:' + str(uid)  #将int转化为string
    colors = ('red','green')
    infos = {'nowcoder':'abc','google':'def'}
    #将参数传入模板中，本程序为profile.html;
    return render_template('profile.html',uid=uid,colors=colors,infos=infos)

@app.route('/request/')
def request_demo():
    key = request.args.get('key','default')
    res = request.args.get('key','default') + '<br/>'
    res = res + request.url + '++' + request.path + '<br>'
    for property in dir(request):
        res = res + str(property) + ' ||  ' +  str(eval('request.' + property))  + '<br>'
        #eval()将字符串str当成有效的表达式来求值并返回计算结果,如eval('1' + 2) 返回3
    response = make_response(res)
    response.set_cookie('nowcoderid',key)
    response.status = '404'
    response.headers['nowcoder'] = 'hello!!'
    return response

#重定向，即跳转,301永久跳转，302临时跳转
@app.route('/newpath')
def newpath():
    return 'newpath'

@app.route('/re/<int:code>')
def redirect_demo(code):
    return redirect('/newpath',code=code)

@app.errorhandler(400)
def exception_page(error):
    return 'exception'

@app.errorhandler(404)
def page_not_found(error):
    print error
    return render_template('not_found.html',url=request.url),404

@app.route('/admin/')
def admin():
    key = request.args.get('key')
    if key == 'admin':
        return 'hello admin'
    else:
        raise ValueError()
    return 'xx'

@app.route('/login')
def login():
    app.logger.info('log success')
    flash('登陆成功','info') #把消息放入消息队列，在首页中取消息，第二个参数为类型
    return 'ok'
    #return redirect('/')  #重定向到首页

@app.route('/log/<level>/<msg>/')
def log(level, msg):
    dict = {'warn': logging.WARN, 'error': logging.ERROR, 'info': logging.INFO}
    if dict.has_key(level):
        app.logger.log(dict[level], msg)
    return 'logged:' + msg

#error信息会出现在error,warn,info文件中，warn信息会出现在warn,info文件中，info信息只会出现在info文件中
#error>warn>info
def set_logger():
    info_file_handler = RotatingFileHandler('C:\\Users\\wangtuanfei\\Desktop\\logs\\info.txt')
    info_file_handler.setLevel(logging.INFO)
    app.logger.addHandler(info_file_handler)

    warn_file_handler = RotatingFileHandler('C:\\Users\\wangtuanfei\\Desktop\\logs\\warn.txt')
    warn_file_handler.setLevel(logging.WARN)
    app.logger.addHandler(warn_file_handler)

    error_file_handler = RotatingFileHandler('C:\\Users\\wangtuanfei\\Desktop\\logs\\error.txt')
    error_file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(error_file_handler)

if __name__ == '__main__':
    set_logger()
    app.run(debug=True)