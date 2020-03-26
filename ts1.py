import socket
import sys

#* .AF_INET corresponds to IPV4
#* SOCK_STREAM corresponds to TCP

def convertFileToArray(file_path):
    f = open(file_path, "r")

    result = []

    contents = f.readlines()

    for line in contents:
        line = line.rstrip('\n')
        line = line.rstrip('\r')

        # split current line in file on space character
        splitString = line.split()

        result.append(splitString)

    f.close()
    return result

def getDomainFromTable(dns_table, server_domain):
    for row in dns_table:
        hostname = row[0]
        ip_address = row[1]
        flag = row[2]

        if(server_domain.upper() == hostname.upper()):
            entry = ' '.join(row)
            return entry

    return False

def server():
    file_path = "PROJ2-DNSTS1.txt"

    listen_port = int(sys.argv[1])

    dns_table = convertFileToArray(file_path)

    # create a socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[TS1]: TS1 Server socket created")
    except s.error as err:
        print('{} \n'.format("socket open error ",err))

    #? bind the socket to an ip address and port number, using tuples: s.bind(<ip_address>, <port_number>)
    s.bind((socket.gethostname(), listen_port))

    host = socket.gethostname()
    print("[TS1]: TS1 Server host name is: " + host)

    ip_address = (socket.gethostbyname(host))
    print("[TS1]: TS1 Server IP address is " + ip_address)

    #* print('Server is Listening...')
    s.listen(1)

    #? Server will listen forever
    while True:
        print("[TS1]: TS1 Server is listening...")

        #? If a connection is heard, the ls_socket object and ip_address from the connection are unpacked into
        #? the 'ls_socket' and 'address' variables
        ls_socket, address = s.accept()
        print "[TS1]: Got a connection request from the server at", address

        #? recieving word given by server
        server_domain = ls_socket.recv(100).decode('utf-8')
        print "\n[TS1]: Domain recieved from server: " + server_domain

        #? search for domain in dns_table
        dns_ipaddress = getDomainFromTable(dns_table, server_domain)

        if(dns_ipaddress == False):
            #? If DNS hasn't been found, do nothing/send nothing back to LS
            print "[TS1]: Could not find domain '" + server_domain + "'\n"
            pass
            # serverMsg = server_domain + ' - Error:HOST NOT FOUND'
            # print "[TS1]: Could not find domain. Sending '" + serverMsg + "' back to server\n"
            # ls_socket.send(serverMsg.encode('utf-8'))
        else:
            serverMsg = dns_ipaddress
            print "[TS1]: Found domain.\n> Sending '" + serverMsg + "' back to LS server\n"
            ls_socket.send(serverMsg.encode('utf-8'))

        ls_socket.close()

    s.close()
    exit()

server()
