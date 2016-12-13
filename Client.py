# module that provides easy access to command-line arguments
import sys
from socket import *
# include variables from 'globals/py'
from globals import *

serverDomainName = None
portNumber = None

#checks command line arguments for a server name and the correct port number
def parseCommandLineArgs():
    global serverDomainName
    global portNumber
    if len(sys.argv) != 3: 
        print "Need two command line arguments"
        sys.exit()
    if int(sys.argv[2]) != 17555:
        print "wrong port number"
        sys.exit()
    # hostname of SMTP Server that will process the email messages
    serverDomainName = sys.argv[1]
    # my port number: 8000 + last 4 digits of my PID
    portNumber = int(sys.argv[2])
    parseServerDomainName(serverDomainName)
    print serverDomainName
    
def parseServerDomainName(domainName):
    if "." in domainName:
        domainName = domainName.split(".")
        alphaDomain = domainName[0]
        #check for only <a> in <a> <let-dig-str>
        if alphaDomain.isalpha() == False:
           print domainError
           sys.exit()
        for x in xrange(1, len(domainName)):
            if domainName[x].isalpha() == False and domainName[x].isdigit() == False:
                print domainError
                sys.exit()
    else:
        for char in domainName:
            if char.isalpha() == False and char.isdigit() == False and char != ".":
                    print domainError
                    sys.exit()

def createTCPSocketToServer():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverDomainName, portNumber))
    #print 'test'
    serverGreeting = clientSocket.recv(1024)
    print serverGreeting
    clientSocket.close()


# client prompts user to enter in contents of email message
def main():
    print fromPrompt,
    sender = str(raw_input())
    while parseEmailAddress(sender, "sender") == False:
        print fromPrompt,
        sender = str(raw_input())
    print toPrompt,
    recipients = str(raw_input())
    while parseRecipients(recipients) == False:
        print toPrompt,
        recipients = str(raw_input())
    print subjectPrompt,
    subject = str(raw_input())
    print messagePrompt,
    # blank line seperating header lines from body of email message
    message = "\n"
    while True:
        messageLine = str(raw_input())
        if checkForPeriod(messageLine) == True:
            # remove final newline from message body
            message = message[:-1]
            break
        else:
            message += messageLine + "\n"
    print message


#checks for <CLRF> '.' <CLRF>   
def checkForPeriod(str):
    if len(str) == 1 and str == ".":
        return True
    else:
        return False

def parseRecipients(recipients):
    recipients = recipients.replace(" ", "")
    recipients = recipients.split(",");
    for x in xrange(0, len(recipients)):
        if parseEmailAddress(recipients[x], "receiver") == False:
            return False
    return True


def parseEmailAddress(str, senderOrReceiver):
    if " " in str or "@" not in str:
        print senderOrReceiver + " email must contain the @ character"
        return False
    #split mailBox into <local-part> and <domain>
    mailBox = str.split("@")
    #check for empty <local-part> and empty <domain>
    for x in xrange(0,len(mailBox)-1):
        if mailBox[x] == "":
            print senderOrReceiver +" email must contain a domain name"
            return False
    #Check <local-part>
    localPart = mailBox[0]
    if (is_ascii(localPart) == False or specialChars(localPart) == True): 
        print "must type in ASCII characters only, and no special characters"
        return False
    #Check <domain>
    domain = mailBox[1]
    #check for existence of '.' in <domain>. If '.' exists, split the domain by '.'
    if "." in domain:
        domain = domain.split(".")
        alphaDomain = domain[0]
        #check for only <a> in <a> <let-dig-str>
        if alphaDomain.isalpha() == False:
            print "first part of domain name must be alphanumeric"
            return False
        for x in xrange(1, len(domain)):
            if domain[x].isalpha() == False and domain[x].isdigit() == False:
                print "domain name must contain alphanumeric characters or a digit from 0-9"
                return False
    else:
        for char in domain:
            if (char.isalpha() == False and char.isdigit() == False and char != "."):
                print "domain name must contain alphanumeric characters or a digit from 0-9"
                return False
    # @param str is a valid sender
    return True

#Function that checks whether all characters in a string are ASCII
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

#Function that checks whether any characters in a string are special as defined in spec.
#If so, function returns True. Else, it returns False
def specialChars(string):
    specialChars = '<>(|)[]\.,;:@"'
    for c in string:
        if c in specialChars:
            return True
    return False

parseCommandLineArgs()
main()
createTCPSocketToServer()
