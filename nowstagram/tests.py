# - * -encoding=UTF-8

import unittest
from nowstagram import app;
# 测试流程，1.初始化数据 2.执行要测试的业务 3.验证测试的数据 4.清理数据
class NowstagramTest(unittest.TestCase):
    def setUp(self):
        print 'setup'

    def tearDown(self):
        print 'tearDown'

    def test_1(self):
        print 'test1'

    def test_2(self):
        print 'test2'
