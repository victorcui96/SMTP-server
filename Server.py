from socket import *
portNumber = 17555
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', portNumber))
# server is listening for one incoming TCP request, only deal with one client at a time
serverSocket.listen(1)
print 'server is ready to receive'
while True:
	connectionSocket, addr = serverSocket.accept()
        print "Got connection from: ", addr
	connectionSocket.send('220' + gethostname());
