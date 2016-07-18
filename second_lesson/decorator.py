# - * -encoding=UTF-8

'''装饰器的作用就是为已经存在的对象添加额外的功能，而不修改原有函数  可以理解成嵌套函数
    def timeit(func):
        def wrapper():
            start = time.clock()
            func()
            end =time.clock()
            print 'used:', end - start
        return wrapper

    @timeit  #@是装饰器语法糖
    def foo():
        print 'in foo()'

    foo()
    这里相当于foo = timeit(foo); foo()
'''

def log(level,*args,**kvargs): #处理带参数的装饰器
    def inner(func):
        '''
        *无名字的参数,形如hello('no',2),用tuple形式访问
        **有名字的参数,形如hello(name='nowcoder',age=2),用dict形式访问
        :param func:
        :return:
        '''
        def wrapper(*args,**kvargs): #可变 参数
            print level,'befor calling',func.__name__
            print level,'args',args,'kvargs',kvargs
            func(*args,**kvargs)
            print level,'end calling',func.__name__
        return  wrapper
    return inner

@log(level='INFO')
def hello(name,age): #带参数
   print 'hello',name,age

if __name__ == '__main__':
    hello(name='nowcoder',age=2)  #=log(hello)