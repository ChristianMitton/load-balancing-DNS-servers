import socket
import sys

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

def clearFile(file_path):
    open(file_path, 'w').close()

def client():
    clearFile("RESOLVED.txt")

    file_path = "PROJ2-HNS.txt"    
    
    ls_host_name = sys.argv[1] + ""

    ls_listen_port = int(sys.argv[2])

    # ts_listen_port = int(sys.argv[3])

    host_names = convertFileToArray(file_path)    

    for user_domain in host_names:          
        user_domain = user_domain[0]    
        # print("user domain: " + user_domain)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # print("[C]: Client socket created")

        except s.error as err:
            print('{} \n'.format("socket open error ",err))
        
        #? pass in IP and port you want to connect to
        # connection = (socket.gethostbyname(socket.gethostname()), ls_listen_port)
        connection = (socket.gethostbyname(ls_host_name), ls_listen_port)
        s.connect(connection)
        
        #? sending user domain to server        
        s.send(user_domain.encode('utf-8'))

        #? recieving message from server
        ls_server_response = s.recv(100)

        serverMsg = ls_server_response.decode('utf-8')

        splitString = serverMsg.split() 

        print("serverMsg: " + serverMsg)  

        f = open("RESOLVED.txt", 'a+')
        f.write(serverMsg + '\n')
        f.close()     

        # if(splitString[2] == "NS"):
        #     # Connect to TS server
        #     TSHostName = splitString[0]
            
        #     try:
        #         ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #         # print("[C]: Client socket created")
        #     except ts.error as err:
        #         print('{} \n'.format("socket open error ",err))   
            
        #     connection = (socket.gethostbyname(TSHostName), ts_listen_port)
        #     ts.connect(connection)

        #     ts.send(user_domain.encode('utf-8'))

        #     ts_server_response = ts.recv(100)

        #     decodedWord = ts_server_response.decode('utf-8')
            
        #     f = open("RESOLVED.txt", 'a+')
        #     f.write(decodedWord + '\n')
        #     f.close()
        # else:            
        #     f = open("RESOLVED.txt", 'a+')
        #     f.write(decodedWord + '\n')
        #     f.close()
        

        s.close()
    
    exit()

client()

# print("Arguments:\n> " + sys.argv[0] + "\n> " + sys.argv[1])