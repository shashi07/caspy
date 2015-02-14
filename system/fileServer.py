from socket import *
from time import ctime
import pickle
import dbconnect
import srfunc
import struct

HOST = 'localhost'
PORT = 28812
BUFSIZE = 1024
ADDR = (HOST, PORT)
tcpTimeSrvrSock = socket(AF_INET,SOCK_STREAM)
tcpTimeSrvrSock.bind(ADDR)
tcpTimeSrvrSock.listen(50)
# data format : (blockdata,hash,block_no,filename,dirstructure,username)
while True:
  print 'waiting for connection...'
  tcpTimeClientSock, addr = tcpTimeSrvrSock.accept()
  print '...connected from:', addr
  request = tcpTimeClientSock.recv(BUFSIZE)
  print request 
  if request == "POST" :
      while True:
        data = tcpTimeClientSock.recv(BUFSIZE)
        if not data:
          break
        data = pickle.loads(data)
        print data

        dir_id = dbconnect.insertInDir(data[5],"root",data[5])
        pname = data[5]
        if data[4] is not None :
            a = data[4].split('/')
            for i in a :
                dir_id = dbconnect.insertInDir(i,pname,data[5])
                pname = i
        print dir_id
        
        f_id = dbconnect.insertInFiles(data[3],dir_id,0)
        h_id = dbconnect.checkHash(data[1])
        if h_id is None :
            h_id = dbconnect.insertInHashes(data[1],len(data[0]))
            f = open("Files/"+data[1],"wb+")
            f.write(data[0])
            f.close()
            message = "created block with hash = %s " %(data[1],)
        else :
            message = "Block Exists."
        dbconnect.insertInBlocks(data[2],f_id,h_id)

        tcpTimeClientSock.send('[%s] %s' % (ctime(), message))
  elif request == "GET" :
      while True:
        fname = tcpTimeClientSock.recv(BUFSIZE)
        fname.strip()
        print fname
        message = "yeah it runs"
        if not fname:
          break
        a = dbconnect.selectAllBlocks(fname,"shashi","root","shashi")
        print len(a)
        i = len(a)/BUFSIZE;
        print i
        for j in range(i+1):
            data = a[j*BUFSIZE:j*BUFSIZE+BUFSIZE]
            print len(data)
            #print tcpTimeClientSock.send(data)
            srfunc.send_msg(tcpTimeClientSock,data)
            if j==i:
              print "end"
              #tcpTimeClientSock.send("True")
              srfunc.send_msg(tcpTimeClientSock,"True")
            else :
              srfunc.send_msg(tcpTimeClientSock,"False")
  '''elif request == "LS" :
      while True:
        uname = tcpTimeClientSock.recv(BUFSIZE)
        uname.strip()
        print fname
        message = "yeah it runs"
        if not fname:
          break
        a = dbconnect.showfiles(uname,"root",uname)
        print len(a)
        i = len(a)/BUFSIZE;
        print i
        for j in range(i+1):
            data = a[j*BUFSIZE:j*BUFSIZE+BUFSIZE]
            print len(data)
            #print tcpTimeClientSock.send(data)
            srfunc.send_msg(tcpTimeClientSock,data)
            if j==i:
              print "end"
              #tcpTimeClientSock.send("True")
              srfunc.send_msg(tcpTimeClientSock,"True")
            else :
              srfunc.send_msg(tcpTimeClientSock,"False")
                  
        #message = "yeah it runs"'''
        #tcpTimeClientSock.send('[%s] %s' % (ctime(), message))
  tcpTimeClientSock.close()
tcpTimeSrvrSock.close()
