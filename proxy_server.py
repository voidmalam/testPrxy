#!/usr/bin/python 

###############################################################################
# filename  : proxy_server.py
# author    : m m alam
# purpose   : creating a proxy server to request data 
# date      : 2016 Jan 4
###############################################################################



import os
import sys
import socket
import thread

# maximum number of bytes will be received at a time 
BUFFER_LENGTH = 4294967296 

# maximum number of connections queue will hold
QUEUE_LENGTH = 50           
 
# set to True to see the debug msgs
DEBUG = True            

    


'''
description     : the main program
param [in/out]  : n/a
'''
#start main

def main():

    # check the length of command running
    if (len(sys.argv)<2):
        print "USAGES   :: python proxy_server.py <port_number>" 
        print "WARNING  :: No port assigned using :8080 as default http port." 
        port = 8080
    else:
        # assign port number from command line argument
        port = int(sys.argv[1]) 

    # host and port info. Kept blank for localhost
    # TODO mohammad : create a local ip 
    host = ''               
    host_name = 'localhost'
    
    if host == '':
        print "Proxy Server Running on :: ",host_name,":",port
    else:
        print "Proxy Server Running on :: ",host,":",port

    try:
        # create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # associate the socket to host and port
        s.bind((host, port))

        # listenning to the socket
        s.listen(QUEUE_LENGTH)
    
    except socket.error, (value, message):
        if s:
            s.close()
        print "ERROR    :: Socket ceation process failed with :", message, "message."
        sys.exit(1)

    # get the connection from client
    while True:
        conn, client_addr = s.accept()

        # create a thread to handle request
        thread.start_new_thread(proxy_server_thread, (conn, client_addr))
        
    s.close()

#end main

'''
description     : show the address, type, command 
param [in]      : type, command, address
'''
#start printout

def printout(type,command,address):
    print address[0],"\t",type,"\t",command

# end printout


'''
description     : A thread to handle request from browser
param [in]      : connection, client_address
'''
#start proxy_server_thread

def proxy_server_thread(conn, client_addr):

    # get the request
    # TODO mohammad : split the event_id from the request to send this id in
    # calendar42 formatted GET request with token for authorization and event_id for unification
    request = conn.recv(BUFFER_LENGTH)

    # parse the first line
    first_line = request.split('\n')[0]

    # get url
    url = first_line.split(' ')[1]

    printout("Request",first_line,client_addr)
    # print "URL:",url
    # print
    
    # find the webserver and port
    # find pos of ://
    http_position = url.find("://")          
    if (http_position==-1):
        temp = url
    else:
        # get the rest of url
        temp = url[(http_position+3):]       
        
    # find the port pos (if any)
    port_pos = temp.find(":")           

    # find end of web server
    webserver_pos = temp.find("/")
    if webserver_pos == -1:
        webserver_pos = len(temp)
    
    # send calendar42 demo server address with event id
    webserver = ""
    port = -1
    # default port
    if (port_pos==-1 or webserver_pos < port_pos):      
        port = 80
        webserver = temp[:webserver_pos]
    
    # specific port
    else:       
        port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
        webserver = temp[:port_pos]

    try:
        # create a socket to connect to the web server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        s.connect((webserver, port))
        
        # send request to webserver
        s.send(request)         
        
        while 1:
            # receive data from web server
            data = s.recv(BUFFER_LENGTH)
            
            # process calendar 42 data here title, event-subscribers name list
            # TODO mohammad : create a function say process_data(data), remember you have to send the request twice 
            # to get event title and event subscribers name list
            
            if (len(data) > 0):
                # send the processed data result to the browser
                conn.send(data)
            else:
                break
        
        # close socket
        s.close()
        
        #close connection
        conn.close()
        
    except socket.error, (value, message):
        if s:
            s.close()
        if conn:
            conn.close()
        printout("Reset",first_line,client_addr)
        sys.exit(1)

#end proxy_server_thread
    
if __name__ == '__main__':
    main()
