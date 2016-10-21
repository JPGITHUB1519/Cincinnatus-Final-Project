import sys
import random
import string
import re
import general
import hashlib
import logging
import time
import os
import operator
# Import the email modules
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.appengine.ext import db
from models.user_model import *
from models.category_model import *
from models.blog_model import *
from general import *
from google.appengine.api import mail
from urllib import urlencode
from libs import httplib2
from models.comment_model import *
# ancestor_key = db.Key.from_path('User', 'some_id')
# import memchache
from google.appengine.api import memcache
SECRET = "PYTHON"
email_sender = 'juanpedro1519@gmail.com'
email_password = 'jp23051519'
# User System function
def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

# make password hash
def generate_hash(name, pw, salt) :
	return hashlib.sha256(name + pw + salt).hexdigest()

# this is the method to generate a hash to the user and password
def make_password_hash(name, pw):
    salt = make_salt()
    h = generate_hash(name, pw, salt)
    return '%s,%s' % (h, salt)

# verify if hash mash with a user 
def valid_password(name, pw, h):
    obtain_salt = h.split(',')[1]
    test_h = generate_hash(name, pw, obtain_salt) + "," + obtain_salt
    if  test_h == h :
    	return True
    return False

# cookie hashing
def hash_str(s):
	# simuling hmac
    return hashlib.sha256(s + SECRET).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    lista = h.split('|')
    if hash_str(lista[0]) == lista[1] :
    	return lista[0]
    return None

# return a random hah
def random_hash():
   random_word = make_salt()
   return hashlib.sha256(random_word + SECRET).hexdigest()

# database stuffs
def sort_dictionary_desc(dic) :
    """ 
        Return a Tuple with the dic Sorted
    """
    return sorted(dic.items(), key = operator.itemgetter(1), reverse = True)

# date to string
def date_to_string(date):
    return date.strftime('%a %b %m %X %Y')

# mailgun
def send_mailgun_complex_message(recipient, subject, html):
    MAILGUN_API_KEY = "key-083013c6e0b9c868f9b1f188fd54fb9a"
    MAILGUN_DOMAIN_NAME = "sandboxc5be1aa9c7be4b0b8683d2078bbd1bfa.mailgun.org"
    http = httplib2.Http()
    http.add_credentials('api', MAILGUN_API_KEY)

    url = 'https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN_NAME)
    data = {
        'from': 'Example Sender <mailgun@{}>'.format(MAILGUN_DOMAIN_NAME),
        'to': recipient,
        'subject': subject,
        'html': html
    }
    resp, content = http.request(url, 'POST', urlencode(data))
    if resp.status != 200:
        raise RuntimeError(
            'Mailgun API error: {} {}'.format(resp.status, content))
    return {"resp" : resp, "content" : content}

def send_mailgun_simple_message(recipient, text):
    MAILGUN_API_KEY = "key-083013c6e0b9c868f9b1f188fd54fb9a"
    MAILGUN_DOMAIN_NAME = "sandboxc5be1aa9c7be4b0b8683d2078bbd1bfa.mailgun.org"
    http = httplib2.Http()
    http.add_credentials('api', MAILGUN_API_KEY)

    url = 'https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN_NAME)
    data = {
        'from': 'Ninja Blog <mailgun@{}>'.format(MAILGUN_DOMAIN_NAME),
        'to': recipient,
        'subject': 'This is an example email from Mailgun',
        'html': html
    }
    resp, content = http.request(url, 'POST', urlencode(data))
    if resp.status != 200:
        raise RuntimeError(
            'Mailgun API error: {} {}'.format(resp.status, content))
    return {"resp" : resp, "content" : content}

def send_simple_email(recipient, subject, text):
    msg = MIMEText(text)
    msg['To'] = recipient
    msg['From'] = email_sender
    msg['Subject'] = subject

    username = email_sender
    password = email_password
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(email_sender, email_password)
    server.sendmail(email_password, recipient, msg.as_string())
    server.quit

def send_html_email(recipient, subject, html):
    msg = MIMEMultipart('alternative')
    msg['To'] = recipient
    msg['From'] = email_sender
    msg['Subject'] = subject
    message_content = MIMEText(html, 'html')
    msg.attach(message_content)
    username = email_sender
    password = email_password
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(email_sender, email_password)
    server.sendmail(email_password, recipient, msg.as_string())