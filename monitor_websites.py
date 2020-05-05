#!/usr/bin/python3
import os, sys, logging
from http.client import HTTPConnection, socket
from datetime import datetime
from smtplib import SMTP

timestamp = datetime.utcnow().strftime("%Y%m%d")

logging.basicConfig(level=logging.DEBUG, filename='checksites_{}.log'.format(timestamp), 
        format='%(asctime)s - %(levelname)s - %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S',
        filemode='a')

def email_alert(message, status):
    fromaddr = ''
    toaddrs = ''
    
    server = SMTP(':587')
    server.starttls()
    server.login('', '')
    server.sendmail(fromaddr, toaddrs, 'Subject: %s\r\n%s' % (status, message))
    server.quit()

def get_site_status(url):
    response = get_response(url)
    try:
        if getattr(response, 'status') == 200 or getattr(response, 'status') == 301:
            logging.info('{} - {}'.format(getattr(response, 'status'),url))
        else:
            logging.error('{} - {}'.format(getattr(response, 'status'),url))
            email_alert(status = getattr(response, 'status'), message=url)
    except AttributeError as ae:
    	logging.error('{} - {}'.format(str(ae),url))
        
def get_response(url):
    '''Return response object from URL'''
    try:
        conn = HTTPConnection(url)
        conn.request('HEAD', '/')
        return conn.getresponse()
    except socket.error:
    	return None
    except:
        logging.error('Bad URL:{}'.format(url))
        exit(1)
        
def get_headers(url):
    '''Gets all headers from URL request and returns'''
    response = get_response(url)
    try:
        return getattr(response, 'getheaders')()
    except AttributeError:
    	return 'Headers unavailable'

def is_internet_reachable():
    '''Checks Google then Yahoo just in case one is down'''
    if get_site_status('www.google.com') == 'down' and get_site_status('www.yahoo.com') == 'down':
        return False
    return True
        
def main(urls):
    # Check sites only if Internet is_available
    if is_internet_reachable():
    	for url in urls:
            get_site_status(url)
    else:
        logging.error('Either the world ended or we are not connected to the net.')
        
if __name__ == '__main__':
    # First arg is script name, skip it
    main(sys.argv[1:])