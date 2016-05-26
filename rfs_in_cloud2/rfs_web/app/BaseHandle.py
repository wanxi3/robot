# _*_ coding:utf-8 _*_
__author__ = 'Eddie'

import Queue
import traceback
import StringIO

class BaseHandle(object):
    def __init__(self):
        self._testcase_list = []
        self._case_name_length = 0
        self._line_length = 100
        self.finish_flag = False
        self.q = Queue.Queue()
        self.stdout = HandleStream(self.q)

    def __iter__(self):
        return iter(self._testcase_list)

    @classmethod
    def setUpClass(cls):
        "Hook method for setting up class fixture before running tests in the class."
        pass

    @classmethod
    def tearDownClass(cls):
        "Hook method for deconstructing the class fixture after running all tests in the class."
        pass

    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        pass

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        pass

    def add_case(self,casename,func,*args,**kwargs):
        if isinstance(func, basestring):
            raise TypeError("tests must be an iterable of tests, not a string")

        if not hasattr(func, '__call__'):
            raise TypeError("{} is not callable".format(repr(func)))

        casename_length = len(casename)
        if casename_length > self._case_name_length:
            self._case_name_length = casename_length
        self._testcase_list.append((casename,func,args,kwargs))

    def run(self):
        self.stdout.write('用例开始执行')
        self.stdout.write(self.split_line)
        try:
            self.setUpClass()
        except:
            return [('setUpClass Faile',False)]

        for case in self._testcase_list:
            r = {}
            try:
                self.stdout.write(case[0])
                self.setUp()
                r = case[1](*case[2],**case[3])
            except Exception,e:
                fp = StringIO.StringIO()
                traceback.print_exc(file=fp)
                self.stdout.write(fp.getvalue())
                r['result'] = False
                r['message'] = e.message
            finally:
                try:
                    self.tearDown()
                except:
                    fp = StringIO.StringIO()
                    traceback.print_exc(file=fp)
                    self.stdout.write(fp.getvalue())
                finally:
                    space_count = self._line_length - len(case[0].encode('utf-8')) - 4
                    if r['result']:
                        result = 'PASS'
                    else:
                        result = 'FAIL'
                    msg = '%s%s%s' %(case[0],' '*space_count,result)
                    self.stdout.write(msg)
                    if result == 'FAIL':
                        self.stdout.write('%s :: 失败原因: %s' %(case[0].encode('utf-8'),r['message']))

                    self.stdout.write(self.split_line)
        try:
            self.tearDownClass()
        except:
            fp = StringIO.StringIO()
            traceback.print_exc(file=fp)
            self.stdout.write(fp.getvalue())
        finally:
            self.stdout.write('全部用例已经执行结束')
            self.finish_flag = True

    @property
    def split_line(self):
        return '=' * self._line_length

    @property
    def case_count(self):
        pass

class HandleStream(object):
    def __init__(self,obj):
        self.obj = obj
        self._make_read = []
        self._mark_finish = False

    def readline(self):
        if self.obj.qsize():
            data = self.obj.get()
            if data == '全部用例已经执行结束':
                self._mark_finish = True
            self._make_read.append(data)
        else:
            data = False
        return data

    def write(self,msg):
        self.obj.put(msg)

    @property
    def mark_read(self):
        return self._make_read

    @property
    def mark_finish(self):
        return self._mark_finish