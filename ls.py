import socket
import sys
import time

#* .AF_INET corresponds to IPV4
#* SOCK_STREAM corresponds to TCP

# def print2DArray(array):
#     for row in array:
#         print '[',
#         for item in row:
#             print item,
#         print ']'
#         print("")

def convertFileToArray(file_path):
    f = open(file_path, "r")

    result = []

    contents = f.readlines()
    for line in contents:        
        line = line.rstrip('\n')
        line = line.rstrip('\r')

        # split line on space
        splitString = line.split()        

        result.append(splitString)
    
    f.close()
    return result    

def getDomainFromTable(dns_table, client_domain):
    for row in dns_table:        
        hostname = row[0]
        ip_address = row[1]
        flag = row[2]

        if(client_domain == hostname):
            entry = ' '.join(row)
            return entry       

    return False

# def getTSHostName(dns_table):
#     for row in dns_table:
#         flag = row[2]
#         if(flag == 'NS'):
#             entry = ' '.join(row)            
#             # print('entry: ' + entry)
#             return entry


def server():    

    listen_port = int(sys.argv[1])    

    ts1_host_name = sys.argv[2] + ""

    ts1_listen_port = int(sys.argv[3])

    ts2_host_name = sys.argv[4] + ""

    ts2_listen_port = int(sys.argv[5])    

    #? create a socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[LS]: Server socket created")
    except s.error as err:
        print('{} \n'.format("socket open error ",err))

    #? bind the socket to an ip address and port number, using tuples: s.bind(<ip_address>, <port_number>)      
    #! Node: socket.gethostname is the ip address of whatever machine server is running on. It doesn't change      
    s.bind((socket.gethostname(), listen_port))    

    host=socket.gethostname()
    print("[LS]: Server host name is: " + host)
    
    ip_address=(socket.gethostbyname(host))
    print("[LS]: Server IP address is " + ip_address)

    s.listen(1)

    #? Server will listen forever
    while True:        
        print("[LS]: Server is listening...")

        #? If a connection is heard, the clientSocket object and ip_address from the connection are unpacked into 
        #? the 'clientsocket' and 'address' variables
        clientsocket, address = s.accept() 
        print "[LS]: Got a connection request from a client at", address

        #? recieving domain given by client
        client_domain = clientsocket.recv(100).decode('utf-8')
        print "\n[LS]: Domain recieved from client: " + client_domain        

        # serverMsg = "I recieved your domain (" + client_domain + ")"
        # print "sending (" + serverMsg + ") back to client.\n"
        # clientsocket.send(serverMsg.encode('utf-8'))

        #TODO listen for 5 seconds
        for i in range(5):
            #? send domain to ts1 server
            try:
                ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # print("[C]: Client socket created")
            except ts1.error as err:
                print('{} \n'.format("socket open error ",err)) 

            connection = (socket.gethostbyname(ts1_host_name), ts1_listen_port)
            ts1.connect(connection) 
            ts1.send(client_domain.encode('utf-8'))

            ts1_server_response = ts1.recv(100)
            ts1_msg = ts1_server_response.decode('utf-8')        

            #? send domain to ts2 server
            try:
                ts2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # print("[C]: Client socket created")
            except ts2.error as err:
                print('{} \n'.format("socket open error ",err)) 

            connection = (socket.gethostbyname(ts2_host_name), ts2_listen_port)
            ts2.connect(connection) 
            ts2.send(client_domain.encode('utf-8'))

            ts2_server_response = ts2.recv(100)
            ts2_msg = ts2_server_response.decode('utf-8')

            if ts1_msg == "" or ts2_msg == "":
                #TODO interrupt timmer, send which ever message is not empty                
                # break            
                pass
            time.sleep(1)

        if ts1_msg != "":
            clientsocket.send(ts1_msg.encode('utf-8'))
        elif ts2_msg != "":
            clientsocket.send(ts2_msg.encode('utf-8'))
        else:
            error_msg = client_domain + " - ERROR: HOST NOT FOUND"
            clientsocket.send(error_msg.encode('utf-8'))

        # search for domain in dns_table
        # dns_ipaddress = getDomainFromTable(dns_table, client_domain)

        # if(dns_ipaddress == False):                        
        #     serverMsg =  getTSHostName(dns_table)
        #     print "[LS]: Could not find domain. Sending '" + serverMsg + "' back to client\n"
        #     clientsocket.send(serverMsg.encode('utf-8'))
        # else:            
        #     serverMsg = dns_ipaddress
        #     print "[LS]: Found domain.\n> Sending '" + serverMsg + "' back to client\n"
        #     clientsocket.send(serverMsg.encode('utf-8'))

        # clientsocket.close()       

    s.close()
    exit()

server()

# Clearing a portnumber in use:
# fuser 50007/tcp -k