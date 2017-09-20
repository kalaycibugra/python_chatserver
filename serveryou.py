import socket
from threading import Thread
import _thread
import threading
import sys

clients=[]
connection_lock = threading.Lock()

class register:

    def __init__(self, ip, port,nick,conne,addr):
        self.ip = ip
        self.port = port
        self.nick = nick
        self.conne=conne
        self.addr=addr#client's address informations

def sendMessage(datax):#sends the message to all usersde
    connection_lock.acquire()
    for connection in clients:#to broadcast incoming message to all clients
        (connection.conne).send(datax)
    print(datax)
    connection_lock.release()
    return
def clientHandler(element):
    while True:
        try:
            data = (element.conne).recv(1024)#recieving message from clients
        except:
            connection_lock.acquire()
            element.conne.close()
            clients.remove(element)#remove client from clients array
            left="SYSTEM->"+element.nick+" left"+"\n"
            leftMsg=left.encode('utf-8')#encode message for the socket
            print(left)
            for connection in clients:
                (connection.conne).send(leftMsg)#send left message to the existing clients
            connection_lock.release()
            return
        curNick=element.nick
        x=data.decode('utf-8')#decode recieved data to string
        e,r=x.split("<")

        t=curNick+"->"+r[:-2]+"\n"

        datax=t.encode('utf-8')#encoding string to byte to send data through the socket

        sendMessage(datax)#for sending modified message to every client

HOST = '127.0.0.1'#localhost
PORT = 6789

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#creating a socket named s
s.bind((HOST, PORT))#connect system's ip with the port
s.listen(10) #max 10 connections

print ("Server is running......")
while(1):

    conn, addr = s.accept()#acccept incoming connection
    x = conn.recv(1024).decode('utf-8')#for recieving data from client
    a=x[0:8]#takes first 8 letters of the data recieved recently
    if(a=="REGISTER"):
        wq,b=x.split("<")
        conn.sendto("Access granted\n".encode('utf-8'),addr)#if data has "REGISTER" in its first 8 letters than server give client access
        c,v,z=b.split(":")
        c=c[1:]
        z=z[:-2]
        element=register(c,v,z,conn,addr)#for each new register an object named register will created.
        print (addr, "is Connected. Adding to registry")
        conn.sendto(("Welcome "+z+"\n").encode('utf-8'),addr)#for sending a welcome message to new client

        connection_lock.acquire()
        clients.append(element)#adding the new client to the clients array
        connection_lock.release()
        threading.Thread(target = clientHandler, args=[element]).start()#i used thread functions to make chat server available for many users
    else:
        conn.sendto("Access denied\n".encode('utf-8'),addr)#sends an Access denied message if client's first message doesn't start with "REGISTER"
        conn.close()#to close client's connection
s.close()#for closing the socket
