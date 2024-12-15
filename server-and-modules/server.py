###TODO###
###add text file download support (reading bytes and encoding fails)
###add upload support
###clean shit up, restructure file org, make windows ver
###implement network support (encryption)
###fix "config" in client, add more commands like move, read, or edit (for text files)
###add chat support cause experience
###add mini games exp
###fuck it just copy most linux commands
###make a website
###OH! oh fuck, create user function. i forgor

###KNOWN ERRORS
###might not have data or cannot access local variable 'cmd2' where it is not associated with a value
###KNOWN ERRORS

from socket import AF_INET as ipv4 #changing function names to what they literally represent
from socket import SOCK_STREAM as tcp
import sys
import time  # noqa: F401
import base64  # noqa: F401
import socket as netcom #netcom = networkcommunication cause it makes more sense instead of socket or socket object
from collections import Counter #Counter(string) is used for counting characters in a hash
import cmdhandler as handle
isloggedin = False
byteformat = ''
buffer = 64
serverdir = '/config/'
##IMPORTS ABOVE
##
##MISC FILE WRITES & OTHER START

def byte_calc(data):
     global byteformat, byte
     byte = data
     if byte < 1000:
          byteformat = 'bytes'
     elif byte > 1000 and byte < 1000000:
          byte = byte / 1000
          byteformat = 'kilobytes'
     elif byte > 1000000 and byte < 1000000000:
          byte = byte / 1000000
          byteformat = 'megabytes'    
def store_cmd(reccmd):
     with open(f'{serverdir}trasmissionlog.txt', 'a') as cmdis:
          cmdis.write(f"<<CMD FROM CLIENT RECV>>\ncommand:{reccmd} recv from {client_ip}, {byte} {byteformat} recieved\n<<RECV CMD FROM CLIENT END>>\n")
def store_res(resdata, *datatype):
     with open(f'{serverdir}trasmissionlog.txt', 'a') as res:
          res.write(f"<<RESULT DATA BELOW>>\n\n\n\n{resdata}\n\n\n\nsent to {client_ip} :: {byte} {byteformat}\ndata type:{datatype}<<RESULT DATA END>>\n")
def store_bytes_recv_file(): 
     with open(f'{serverdir}trasmissionlog.txt', 'a') as storebyte:
          storebyte.write(f"<<HANDSHAKE RECV START>>\nhandshake recv:{byte} {byteformat} recieved from {client_ip}\n<<HANDSHAKE RECV END>>\n")
def store_bytes_send_file(): 
     with open(f'{serverdir}trasmissionlog.txt', 'a') as storebyte:
          storebyte.write(f"<<HANDSHAKE SEND START>>\nhandshake sent: {byte} {byteformat} sent to {client_ip}\n<<HANDSHAKE SEND END>>\n")
def store_user_addr_file():
     with open(f'{serverdir}trasmissionlog.txt', 'a') as storedata:
          storedata.write(f"<<CONFIRM USER START>>\n{user} as {client_ip}\n<<CONFIRM USER END>>\n")
def store_response(responsedata):
     with open(f'{serverdir}trasmissionlog.txt', 'a') as res:
          res.write(f"<<RESPONSE DATA BELOW>>\n{responsedata}\nsent to {client_ip} :: {byte} {byteformat}\n<<RESPONSE DATA END>>\n")

##MISC FILE WRITES & OTHER END
##
##CONNECT AND SYNC START

def get_port_ip_input():
     global client_ip, endpoint1, getport, getip
     #getport = input('listen port number: ')
     #getip = input('listen ip: ') TESTING
     getip = 'localhost'
     getport = 12345
get_port_ip_input() #declaring seperatly so when prompting a retry we dont have to reinput the information
def listen_for_connsync():
     global client_ip, endpoint1, isconnected, char, byte, byteformat, client_socket
     endpoint1 = netcom.socket(ipv4, tcp)#endpoint is global so we can use a function to close the server in a seperate program
     endpoint1.bind((getip, int(getport))) #will have to filter real ip addresses (int) and localhosts later
     char = ''
     isconnected = ''
     try: 
          print('binded and listening')
          endpoint1.listen(1)
          client_socket, client_ip = endpoint1.accept() #accept() creates a new socket because endpoint1 is used for listening 
          client_socket.settimeout(1)
          #and a new socket needs to be created to sustain a connection
          isconnected = client_socket.recv(33280)#33280 is how much data i can send in one second uneeded for specifically this recv data since it should                     
     except: # noqa: E722
          pass
     isconnected = isconnected.decode('utf-8')
     if 'True' in isconnected: 
          handshake()
          return
     else: 
          print('failed in listen_for_con')
          isconnected = False        
def handshake():
     global connected
     try:
          connected = 'True'
          byte_calc(len(connected))
          store_bytes_send_file()
          connected = connected.encode('utf-8')
          client_socket.send(connected)
     except netcom.error as e:
          server_retry(e)         
def server_retry(exception):
     print('server error:', exception)
     print('client not responding.')
     retry = input('retry? ')
     retry = retry.lower()
     if 'y' in retry:
          endpoint1.close
          client_socket.close
          listen_for_connsync()
     else:
          print('exited')
          sys.exit() 

##CONNECT AND SYNC END
##
##LOGIN START

def cmd_login_info_recv():
     global client_socket, client_ip, byte, byteformat, user
     if isloggedin == False:  # noqa: E712
          try:
               client_socket.settimeout(1.0)
               receivingdata = client_socket.recv(3200)
          except Exception as e:  # noqa: E722
               print('failed in cmd_login_recv \n', e)
          recvdata = receivingdata.decode('utf-8') 
          recvdata = recvdata.replace(' ',"") # noqa: F841
          recvdata = recvdata.strip()
          user, passw = recvdata.split("#")
          confirm_login(user, passw)
          byte_calc(len(recvdata))
          store_bytes_recv_file()
          cmd_login_info_recv()
               
     else:
          client_socket.send(str(isloggedin).encode('utf-8'))
          return
def confirm_login(recvuser, recvpass):
     global isloggedin
     with open(f'{serverdir}storedusers.txt', 'r') as passverifying:
          loginverify = passverifying.readlines()
          for loginis in loginverify: 
               usercomp, passcomp = loginis.strip().split('::')
               if passcomp == recvpass and usercomp == recvuser:
                    isloggedin = True
                    return
               else:
                    print('login failed')
                    isloggedin = False

##LOGIN END
##
##USER COMMAND START

def cmd_from_client_recv():
     global cmd
     param = ''
     while True:
          client_socket.settimeout(None)
          try:
               recvcmd = client_socket.recv(10000)
               byte_calc(len(recvcmd))
               store_cmd(recvcmd)
               recvcmd = recvcmd.decode('utf-8') 
               cmd, end = recvcmd.strip().lower().split('&&&')
               if '!:cmd:!' in cmd:
                    cmd, *cmd2 = cmd.split('!:cmd:!')
               print(cmd, *cmd2)
                    
               if cmd and '<<<' in end:
                    havedata = True
                    print(cmd)
                    xcmd = cmdpassdict.get(*cmd2)
                    if xcmd:
                         return xcute(*cmd2)
                    else:
                         if param == '':
                              cmdresult = handle.cmdloop(cmd, *cmd2) #recvcmd not used so can be dropped
                              cmd_to_client_send(handle.result)
                         else:
                              cmdresult = handle.cmdloop(cmd) #all cmd handler
                              cmd_to_client_send(handle.result)
                              param = ''
             
          except Exception as e:
               havedata = False
               result = f'might not have data or {e}'
               cmd_to_client_send(result)
def cmd_to_client_send(res):
     byte_calc(len(res))
     store_res(res, 'file data')
     end = '<<<'
     if '<filename>' in res:
          res = res + "&&&" + end
          client_socket.sendall(res.encode('utf-8'))
          
          
     else:
          res = str(res) + '&&&' + end   
          store_res(res)
          client_socket.send(res.encode('utf-8'))

##USER COMMAND END
##
##PROGRAM RUN
       
#if __name__ == '__main__': #uncomment when importing to execute.py
#     listen_for_connsync()
listen_for_connsync()                
cmd_login_info_recv()
cmd_from_client_recv()
