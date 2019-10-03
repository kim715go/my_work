from pivotProgram2 import ui

import ftplib
from time import time

from PyQt5 import QtCore, QtWidgets

class MyFTP_TLS(ftplib.FTP_TLS):
    """Explicit FTPS, with shared TLS session"""
    def ntransfercmd(self, cmd, rest=None):
        conn, size = ftplib.FTP.ntransfercmd(self, cmd, rest)
        if self._prot_p:
            conn = self.context.wrap_socket(conn,
                                            server_hostname=self.host,
                                            session=self.sock.session)  # this is the fix
        return conn, size

server = MyFTP_TLS(host = '147.46.20.65')
server.connect(port = 6421)
server.auth()
server.login(user='aiees1234', passwd='aiees1234')
server.prot_p()
server.encoding='utf-8'