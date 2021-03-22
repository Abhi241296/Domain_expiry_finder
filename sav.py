#This script only works for .com and .net as valid domain names(as the task specified .com domain names)
import socket, re, datetime

#Function to connect to interNIC and fetch the domain registry information
def lookup(server , domain):
    #socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #establishing a connection with the service
    s.connect((server, 43))
    
    #sending request to the service
    s.send(domain.encode('utf-8') + '\n'.encode('utf-8'))

    #response
    res = ''
    while len(res)<10000:
        chunk = s.recv(100).decode('utf-8')
        if(chunk == ''):
            break
        res = res + chunk

    return res

#Function to clean the domain name, call the lookup service, and finally clean the output and return the expiration date as a datetime object
def expiry(domain):
    #this cleans the input to make it acceptable by the service
    domain = domain.replace('https://', '')
    domain = domain.replace('http://', '')
    domain = domain.replace('www', '')

    #to get the domain type
    d_type = domain[-3:]

    #this checks if the domain name is one of the three (acceptable by interNIC)
    if(d_type == 'com' or d_type == 'net'):

        #interNIC service which has the domain registry information for gLTD (ending in .com, .net)
        s_name = 'whois.internic.net'
        
        #calling the lookup function
        res = lookup(s_name, domain)

        #cleaning the response to only get the registry expiration date (since the repsonse format is set this will work always)
        res = res.splitlines()
        res = res[6].split(': ', 1)
        res = res[1]

        #converting the string to datetime object and returning it
        expiry_date = datetime.datetime.strptime(res, '%Y-%m-%dT%H:%M:%SZ')
        
        #print(type(expiry))
        return expiry_date
    
    else:
        return "Invalid Domain name please try again"


#driver code
domain_name = input("Enter a domain name: ")
print(expiry(domain_name))