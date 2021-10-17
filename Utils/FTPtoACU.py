# -*- coding: UTF-8 -*-
from ftplib import FTP
import os
import sys
import time
import socket


class FTPtoACU(object):
    """
        The monitoring and management server
        uses FTP to send antenna guidance data files to ACU
    """

    def __init__(self, host, port):
        """
        init the FTP client
        """
        self.host = host
        self.port = port
        self.ftp = FTP()
        self.ftp.encoding = 'gbk'
        self.err = None
        self.log_file = open("log.txt", "a")

    def login(self, username, password):
        """
            init the FTP Client
        """
        try:
            socket.setdefaulttimeout(5)
            self.ftp.set_pasv(True)

            self.debug_print('Start trying to connect to %s' % self.host)
            self.ftp.connect(self.host, self.port)
            self.debug_print('Successfully connected to %s' % self.host)

            self.debug_print('Start trying to log in to %s' % self.host)
            self.ftp.login(username, password)
            self.debug_print('Successfully logged in to %s' % self.host)

            self.debug_print(self.ftp.welcome)
        except Exception as e:
            self.err = e
            print("FTP connection failed with error ：%s" % e)

    def download_file(self, local_file, remote_file):
        """
        Download file from FTP
        """
        self.debug_print("Download_file \n \
                    local_path = %s \n \
                    remote_path = %s " % (local_file, remote_file))
        try:
            self.debug_print('Download file %s ' % os.path.basename(local_file))
            bufsize = 1024
            file_handler = open(local_file, 'wb')
            self.ftp.retrbinary('RETR %s' % remote_file, file_handler.write, bufsize)
            file_handler.close()
        except Exception as e:
            self.debug_print('Download file with error：%s ' % e)
            return

    def upload_file(self, local_file, remote_file):
        """
        Upload file to FTP
        """
        if os.path.isfile(local_file):
            self.debug_print("Upload_file \n \
                    local_path = %s \n \
                    remote_path = %s " % (local_file, remote_file))
            try:
                self.debug_print('Download file %s ' % os.path.basename(local_file))
                buf_size = 1024
                file_handler = open(local_file, 'rb')
                self.ftp.storbinary('STOR %s' % remote_file, file_handler, buf_size)
                file_handler.close()
                self.debug_print('Upload: %s successfully' % local_file)
            except Exception as e:
                self.debug_print('Upload file with error：%s ' % e)
                return
        else:
            self.debug_print('%s not exist' % local_file)
            return

    def close(self):
        """
        EXIT FTP
        """
        self.debug_print("EXIT FTP")
        self.ftp.quit()

    def debug_print(self, s):
        """
        Print log
        """
        self.write_log(s)

    def deal_error(self, e):
        """
        Handling error exception
        """
        log_str = 'An error occurred: %s' % e
        self.write_log(log_str)
        sys.exit()

    def write_log(self, log_str):
        """
        Write log
        """
        time_now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
        format_log_str = "%s %s \n " % (time_now, log_str)
        print(format_log_str)
        self.log_file.write(format_log_str)


if __name__ == "__main__":
    f = FTPtoACU("172.20.208.194", 9999)
    f.login("yang", "123456")

    f.upload_file("/Users/yangjiahao/PycharmProjects/tle-eph/CSS(TIANHE-1)_20211005045905.eph",
                  "/Users/yangjiahao/PycharmProjects/toACU/CSS(TIANHE-1)_20211005045905.eph")
    f.download_file("/Users/yangjiahao/PycharmProjects/tle-eph/CSS(TIANHE-1)_20211003034847.eph",
                    "/Users/yangjiahao/PycharmProjects/toACU/CSS(TIANHE-1)_20211003034847.eph")

    f.close()
