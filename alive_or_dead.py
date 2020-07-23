#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#检测服务器存活情况，分为linux服务器和windows服务器，linux服务器检测ssh端口（22）
#windows服务器检测ping,然后检测3389端口

import telnetlib
import xlrd
import os


linux_ip_server = {}
windows_ip_server = {}
switch_ip = {}

class CHKserverAlive(object):

    def __init__(self,ip_address):
        self.ip_address=ip_address


    def for_linux(self):
        result = b""
        try:
            tm = telnetlib.Telnet(host=self.ip_address,port='22',timeout=4)
            result = tm.read_until(b"\n",timeout=5)
            #print(result)

        except:
            pass

        if b"SSH" in result:
            #print("Linux_server:%s:%s is alive." % linux_ip_server[ip_address],self.ip_address)
            print(linux_ip_server[self.ip_address],self.ip_address,"is alive.")
        else:
            
            print(linux_ip_server[self.ip_address],self.ip_address,"is not alive.")

    def for_windows(self):
        result = b""

        result = os.popen("ping %s" % self.ip_address)
        ans = result.readlines()[-2].strip()
        result.close()
        if ans == '往返行程的估计时间(以毫秒为单位):':
            try:
                tm = telnetlib.Telnet(host=self.ip_address,port='3389',timeout=4)
                res = tm.read_until(b"\n",timeout=5)
                #print(res)
            except:
                res = None

            if res == b"":
                print(windows_ip_server[self.ip_address],self.ip_address,"is alive.")

            else:
                print(windows_ip_server[self.ip_address],self.ip_address,"is not alive.")


        else:
            print(windows_ip_server[self.ip_address],self.ip_address,"is not alive.Please double check by yourself.")


def get_ip_server():

        
        
        #打开IP-server.xlsx文件
        workbook = xlrd.open_workbook(r'.\IP-server.xlsx')

        #定位sheet1
        table = workbook.sheets()[0]

        #获取行数，列数
        rows = table.nrows
        cols = table.ncols

        #获取单元格内容
        for i in range(rows):
            if i==0:
                continue
            else:
                ip = table.cell(i,0).value
                role = table.cell(i,1).value
                os = table.cell(i,2).value

                if os == "windows":
                    
                    windows_ip_server[ip] = role

                elif os == "linux":

                    linux_ip_server[ip] = role

                elif os == "h3c":

                    switch_ip[ip] = role

        return linux_ip_server,windows_ip_server,switch_ip
    
        print("linux:",linux_ip_server.keys)
        print("windows",windows_ip_server.values)
        print("switch",switch_ip.items)
        
if __name__ == '__main__':
    #CHKserverAlive("192.168.0.191").for_linux()
    get_ip_server()
    #print(linux_ip_server.keys)
    for ip in linux_ip_server.keys():
        CHKserverAlive(ip).for_linux()

    for ip in windows_ip_server.keys():
        CHKserverAlive(ip).for_windows()

    #CHKserverAlive("192.168.16.93").for_windows()
