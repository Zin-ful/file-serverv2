import os
import sys  # noqa: F401
import time
import socket as netcom
import base64
#no filtering since we have custom pseudo bash
dirlist = []
filecount = 0
homedir = '/home/raspi/'
userdir = '/home/raspi/'
os.listdir(userdir)
def get_client_from_server(clientip, clientport):
    global ipaddr,port
    ipaddr = clientip
    port = clientport
def printFile(file):
    global result
    counting = 0
    for fileindex in dirlist:
        if file == fileindex:
            with open(file, 'r') as filedata:
                result = print(str(filedata.read()))
                return result
        else:
            counting += 1
            if counting < filecount:
                pass
            else:
                result = 'file not found'
                return result
                break    
def send(*file):
    global result
    if '!:filesendinfo:!' in file:
        filename, filedata = file.split('!:filesendinfo:!')
        filedata = base64.b64decode(filedata)
        with open(f'{userdir}{filename}', 'wb') as fileto:
            fileto.write(filename)
        
        result = f'{filename} uploaded'
    else:
        result = 'upload failed'
    return result 
def get (*filereq):
    global result
    filereq = str(filereq)
    filename = filereq.strip('()').strip(',').strip("'").strip()
    to_down = userdir + str(filereq)
    filelist = os.listdir(userdir)
    print(filelist)
    if not any('/' in d for d in filename): #turns d into a list making any() applicable. iterates thru dir using d as the temp var
        filename = '/' + filename
    if any(filename in files for files in filelist):#file check to make sure exist
        try:
                with open(to_down, 'rb') as file:
                    filedata = file.read() #Everything below me is fucked (maybe)
                    filedata = base64.b64encode(filedata).decode('utf-8')
                    result = filename + '!:fileinfo:!' + filedata
        except Exception as e:
            result = e
    else:
        result = 'file not found'
    return result
        
        
def currentdir():
    global result
    result = userdir.replace('/home/raspi/', '')  
    return result
def echo():
    global result
    result = echome
    return result
def change(*dir):
    global result, userdir
    if not any('/' in d for d in dir): #turns d into a list making any() applicable. iterates thru dir using d as the temp var
        result = 'directory not found, might be missing "/"'
    elif '/storage' in dir:
        userdir = '/home/raspi/storage/'
        userdirclean = str(userdir.replace('/home/raspi/', ''))
        result = f'directory changed to {userdirclean}'
    elif not '/storage' in dir:
        dir = str(dir)
        dir = dir.strip('()').strip(',').strip("'")
        userdir = homedir + str(dir)
        #refresh(os.listdir(userdir))
        userdirclean = str(userdir.replace('/home/raspi/', '') )
        result = f'directory changed to {userdirclean}'
    else:
        result = 'directory not found, might not exist'

    return result
def listfile(*file):
    global txt, result
    dirlist = os.listdir(userdir)
    result = str(dirlist)
    return result
def info(*information):
    global result
    command = cmd_info_dict.get(information) #returns none, dont know why
    result = command
    return result   
def limit():
    global result
    result = 'empty' 
    return result   
def credits():
    global result
    result = 'made by cxsper and zinful'
    return result
def help():
    global result
    result = 'Current working commands: send, print, echo, change, list, credits, info, limit, config, currentdir, help'
    return result
def config():
    global result
    result = 'config changed successfully, probably'
    return result
    sys.exit()
def userCmd(command, *param):
    
    xcute = cmddict.get(command)
    global result
    if xcute:
        return xcute(*param)#since we omit the () in the dictionary for the functions, we put it here
                    #instead that way we only call the function that the user wants
    else:
        result = 'type "help" for more information'
        return result      
cmddict = {'print':printFile,
           'credits':credits,
           'help':help, #add the () to the user input to call func
           'list':listfile,
           'change':change,
           'get':get,
           'send':send,
           'echo':echo,
           'limit':limit,
           'info':info,
           'pwd':currentdir,
           'config':config
}
cmd_info_dict = {
   'print':f'usage: print filename\nusing the (print) command will print out the data inside a file.\ndoes not work media files or other files that contains encoded data',
   'credits':f'credits displays the names of who created this program',
   'help':f'help lists all working commands',
   'list':f'list will display directories and files inside of a given folder',
   'change':f'usage: change filename\nchange will allow the user to change directories',
   'send':f'usage: send filename\nsend allows users to upload files',
   'echo':f'this ones obvious',
   'get':f'usage: get filename\nget allows users to download files',
   'limit':f'limit informs the user of what this program is capable of and why it uses a fake bash system instead of actual bash',
   'info':f'usage: info filename\ninfo provides information on commands',
   'currentdir':f'currentdir displays the current directory of the user',
   'config':f'changes client config settings, still sends server the data since i dont want to code around it'
}

def cmdloop(servercmd, *servercmd2):
    global result, echome
    while True:
        echome = servercmd
        if 'exit' in servercmd:
            sys.exit
        userCmd(servercmd, *servercmd2)  
        print(result) 
        return result #return not only escapes a function but specifically back to the caller
        if not servercmd:    #more specifically server.py, and returning a var returns its values
            print('no cmd') #to the caller
            pass #move to top
                
if __name__ == '__main__':
    cmdloop()
