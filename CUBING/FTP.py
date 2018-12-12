#!C:/Python27
# coding=gbk

from ctypes import *
import os
import sys
import ftplib
import chardet


class myFtp:
    ftp = ftplib.FTP()
    bIsDir = False
    path = ""

    def __init__(self, host):
        self.ftp.connect(host)

    def Login(self, user, passwd):
        self.ftp.login(user, passwd)
        ftp.encoding = "utf-8"
        ftp.encoding = "gbk"

        print(self.ftp.welcome)

    def DownLoadFile(self, LocalFile, RemoteFile):  # 下载单个文件
        bufsize = 1024
        file_handler = open(LocalFile, 'wb')
        print(file_handler)
        self.ftp.retrbinary("RETR %s" % (RemoteFile), file_handler.write,
                            bufsize)  # 接收服务器上文件并写入本地文件
        file_handler.close()
        print('成功下载文件： "%s"' % RemoteFile)
        self.ftp.delete(RemoteFile)
        return True


    def DownLoadFileTree(self, LocalDir, RemoteDir):  # 下载整个目录下的文件
        print("DownLoadFiles:", RemoteDir)
        if os.path.isdir(LocalDir) == False:
            os.makedirs(LocalDir)
        self.ftp.cwd(RemoteDir)
        RemoteNames = self.ftp.nlst()
        print("RemoteFile", RemoteNames)
        for file in RemoteNames:
            Local = os.path.join(LocalDir, file)
            if self.isDir(file):
                self.DownLoadFileTree(Local, file)
            else:
                self.DownLoadFile(Local, file)
        self.ftp.cwd("..")
        return

    def show(self, list):
        result = list.lower().split(" ")

        if "<dir>" in result:
            self.bIsDir = True

    def isDir(self, path):
        self.bIsDir = False
        self.path = path
        # this ues callback function ,that will change bIsDir value
        self.ftp.retrlines('LIST', self.show)
        return self.bIsDir

    def close(self):
        self.ftp.quit()


if __name__ == "__main__":
    ftp = myFtp('ul.faw-vw.com')
    # ftp.Login('faw-vw.in/xiaoai.zhang', 'fawvw.2018')  # 登录，如果匿名登录则用空串代替即可
    # ftp.DownLoadFileTree(r'D:\01_MProject\GetDmoFromftp\01_SupplierReport',
    #                      '/20180409/01_SupplierReport/')  # 从目标目录下载到本地目录d盘
    ftp.Login('user0315', '9cfv48m')  # 登录，如果匿名登录则用空串代替即可
    ftp.DownLoadFileTree(r'D:\01_MProject\GetDmoFromftp\01_SupplierReport',
                         '/20180315/01_SupplierReport/')  # 从目标目录下载到本地目录d盘

    ftp.close()
    print("ok!")
