#-*- encoding=UTF-8 -*-
import random
import re
'''用BeautifulSoup爬取糗事百科的笑话'''
import requests
from bs4 import BeautifulSoup
from requests import request

def qiushibaikeSpider():
    content = requests.get('http://www.qiushibaike.com').content
    soup = BeautifulSoup(content,'html.parser')

    for div in soup.find_all('div',{'class':'content'}):
        print div.text.strip()  #strip(s[, chars]))中参数为空表示去除字筗串中的空格
        print '--分割--'
#开头#表示单行注释

def demo_string():
    stra = "hello world"
    print stra.capitalize() #首字母大写
    print stra.replace('world','nowcoder')
    strb = '  \n\rhello nowcoder \r\n'
    print 1,strb.lstrip() #移除左边的回车、换行等
    print 2,strb.rstrip() #移除右边（末尾）的回车、换行等
    strc = 'hello w'
    print 3,strc.startswith('hel')
    print 4,strc.endswith('x')
    print 5,stra + strb + strc
    print 6,len(strc)
    print 7,'-'.join(['a','b','c']) #用 - 把字符连起来
    print 8,strc.split(' ') #字符串分割函数
    print 9,strc.find('ello')

def demo_operation():
    print 1,1 + 2,3/4,8 * 2
    print 2,True,not True
    print 3,8 | 2,6 & 4,5 ^ 5

def demo_buildinfunction():
    print 1,max(2,3),min(4,5)
    print 2,len('xxx'),len([1,2,3,3])
    print 3,abs(-2)
    print 4,range(1,10,3)
    print 5,dir(list)
    x = 2
    print 6,eval('x + 3')
    print 7,chr(65),ord('a')

class User:
    type = 'USER'
    def __init__(self,name,uid):
        self.name = name
        self.uid = uid
    def __repr__(self):
        return 'im ' + self.name + ' ' + str(self.uid)

class Admin(User):
    type = 'ADMIN'
    def __init__(self,name,uid,group):
        User.__init__(self,name,uid)
        self.group = group
    def __repr__(self):
        return 'im ' + self.name + ' ' + str(self.uid) + ' ' + self.group

class Guest(User):
    def __repr__(self):
        return 'im ' + self.name + ' ' + str(self.uid)


def create_user(type):
    if type == 'USER':
        return User('u1',1)
    elif type == 'ADMIN':
        return Admin('a1',101,'g2')
    else:
        return Guest(':guest',2)

def demo_random():
    #伪随机种子，每次产生的随机数都是一样的
    #random.seed(1)
    #1 - 100
    print 1,int(random.random() * 100)
    print 2,random.randint(0,200)
    print 3,random.choice(range(0,100,10))
    print 4,random.sample(range(0,100),4)
    a = [1,2,3,4,5]
    random.shuffle(a)
    print 5,a


def demo_re():
    str = 'abdd213abaab3a3rab333'
    p1 = re.compile('[\d]+')
    p2 = re.compile('(\d+)')
    print 1,p1.findall(str)
    print 2,p2.findall(str)


if __name__ == '__main__':
    '''
    user1 = User('u1',1)
    print user1
    admin1 = Admin('a1',101,'g1')
    print admin1
    print create_user('USERx')
'''
    #print 'hello nowcoder'
    # comment
    #demo_string()
    #demo_operation()
    #demo_buildinfunction()
    #demo_random()
    #demo_re()
    print dir(request)