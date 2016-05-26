# -*- coding: utf-8 -*-

import os.path
import tempfile
import time


class Listener:

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, *args):
        filename = args[0]
        self.level = args[1]
        self.outfile = open(filename, 'w')
        self.namespace = ''
    #
    # def start_suite(self, name, attrs):
    #     self.outfile.write("%s '%s'\n" % (name, attrs['doc']))
    #
    # def start_test(self, name, attrs):
    #     tags = ' '.join(attrs['tags'])
    #     self.outfile.write("- %s '%s' [ %s ] :: \n" % (name, attrs['doc'], tags))
    #
    # def end_test(self, name, attrs):
    #     if attrs['status'] == 'PASS':
    #         self.outfile.write('PASS\n')
    #     else:
    #         self.outfile.write('FAIL: %s\n' % attrs['message'])
    #
    # def end_suite(self, name, attrs):
    #     self.outfile.write('%s\n%s\n' % (attrs['status'], attrs['message']))

    # def start_keyword(self,name,attrs):
    #     print name,attrs
    #     for i in range(10):
    #         print i
    #         time.sleep(1)

    def log_message(self, message):
        if 'GET' in message['message']:
            pass
        if self.level == "INFO":
            if message["level"] in ("FAIL", "WARN", "INFO"):
                self.outfile.write(message["timestamp"] + ":" + message["level"] + ":" + message["message"] + "\n")
        elif self.level == "DEBUG":
            if message["level"] in ("FAIL", "WARN", "INFO", "DEBUG"):
                self.outfile.write( message["timestamp"] + ":" + message["level"] + ":" + message["message"] + "\n")
        elif self.level == "TRACE":
            if message["level"] in ("INFO",):
                if 'GET' in message['message']:
                    pass
                else:
                    self.outfile.write(message["timestamp"] + ":" + message["level"] + ":" + message["message"] + "\n")
        else:
            pass

    def close(self):
         self.outfile.close()