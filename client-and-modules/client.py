from socket import AF_INET as ipv4 #changing function names to what they literally represent
from socket import SOCK_STREAM as tcp
import sys
import time
import socket as netcom
import base64
print('client imported')
def config():
    global setuserdir, setip, setport
    setuserdir = input('where do you want files to be downloaded? (full system path)\n ')
    setip = input('what is the server IP Address?\n ')
    setport = input('what is the server port?\n ')
    with open('/home/raspi/file-server/client-and-modules/config/config.txt', 'w') as configfile:
        configfile.write(f'USERDIR@{setuserdir}::True\n') # open file as write since we want to overwrite old config
        configfile.write(f'IPADDR@{setip}::True\n')
        configfile.write(f'PORT@{setport}::True\n')
    

## Does this check on every start up, lets the user have more control
## without reprompting on boot
## causes type error tho

def configread():
    global getip, getport, getdir
    truecount = 0
    with open ('/home/raspi/file-server/client-and-modules/config/clientconfig.txt', 'r') as configcheck:
        configdata = configcheck.readlines()
        if configdata == []:
            config()
        print(configdata)
        for linedata in configdata:
            if "True" in linedata:
                truecount += 1
                if truecount == 3:
                    for line in configdata:
                        setdata, bool1 = line.split('::')
                        if 'USERDIR' in setdata:
                            getdir = setdata.replace('USERDIR@', '')
                        elif 'IPADDR' in setdata:
                            getip = setdata.replace('IPADDR@', '')
                        elif 'PORT' in setdata:
                            getport = setdata.replace('PORT@', '')
            else:
                config()
    

 

def reconnect():
    return 
def getCmd():
    return
def sendCmd():
    while True:
        file = ''
        userinput = input('>>>') #send file here to proccess encoding
        end = '<<<'
        if 'exit' in userinput:
            sys.exit()
        elif 'config' in userinput:
            config()
            print('will have to exit to enact change\nexiting in 5')
            a = 'exit'
            
            connection1.send(a.encode('utf-8'))
            time.sleep(5)
        userinput = userinput + '&&&' + end   
        connection1.send(userinput.encode('utf-8'))
        while True:
            try:
                recvresult = connection1.recv(100000000)
                recvresult = recvresult.decode('utf-8')
                with open('/home/raspi/file-server/client-and-modules/config/errorlog.txt', 'a') as log:
                    log.write(f'recvresult\n') 
                print('passed decode')
                recvresult, end = recvresult.split('&&&')
                print('passed strip/split')
                recvresult = recvresult.strip()
                
                if '!:fileinfo:!' in recvresult and '<<<' in end:
                    file = recvresult
                    filename, filedata = file.split('!:fileinfo:!') #change this so the filename and format are one string, also for updated server command processing
                    filedata = base64.b64decode(filedata) 
                    with open(f'{getdir}{filename}{format}', 'wb') as downfile:
                        downfile.write(filedata)
                    print(f'file downloade in {getdir}\nto change target directory use "config"')
                    
                elif '!:sendfileinfo:!' in recvresult and '<<<' in end:
                    global sendfile
                    sentfile = input('What file?')
                    filename, format = sentfile.split('.')
                    with open(f'{filename}.{format}', 'rb') as filesend:
                        filetosend = filesend.read()
                        filetosend = base64.b64encode(filetosend).decode('utf-8') #change format to have 
                        sendfile = f'{filename}<filename>{filetosend}<filesend>.{format}'
                        connection1.send(sendfile.encode('utf-8'))
                        
                elif recvresult and '<<<' in end:
                    print(recvresult)
                    break
            except Exception as e:
                print ('no data\n',e)
                with open('/home/raspi/file-server/client-and-modules/config/errorlog.txt', 'a') as log:
                    log.write(str(f'<<EXCEPTION>>\n{e}\n<<CMD>>\n{userinput}\n<<CMD>>\n'))
                break
    
    
def connect_to_Host():
    confirmrecv = ''
    confirmsend = ''
    print('trying')
    try:
        connection1.connect((str(getip), int(getport)))
        print('authenticating')
        confirmsend = 'True'
        confirmsend = confirmsend.encode('utf-8')
        connection1.send(confirmsend)
        connection1.settimeout(10.0)
        confirmrecv = connection1.recv(200)
        print(confirmrecv)
        confirmrecv = confirmrecv.decode('utf-8')
        print(confirmrecv)
    except TimeoutError:
        if not confirmrecv:
            print('no data recv')
        print('Auth failure')
    
    if 'True' in confirmrecv:
        print('connected')
        try:
            login = "sin"#input("username: ")
            password = "baxter99"#input("password: ")
            userinfosend = f'{login}#{password}'
            print(userinfosend)
            userinfosend = userinfosend.encode('utf-8')
            connection1.send(userinfosend) #could honestly just encode it outside a variable cause your putting
        #a var to be encoded inside a second var which makes no sense
        #encrpt data before sending over network, bcrypt or write your own
        except connection1.error as e:
            print('error occured \n', e)
            print('connected')
        connection1.settimeout(5)
        isloggedin = connection1.recv(4)
        isloggedin = isloggedin.decode('utf-8')
        if 'True' in isloggedin:
            return
        
    else:
        print('failed, no True in confirmrecv')
        

        

connection1 = netcom.socket(ipv4, tcp) 
configread()
connect_to_Host()
sendCmd()
