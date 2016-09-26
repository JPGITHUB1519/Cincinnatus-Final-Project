import sys
import random
import string
import re
import general
import hashlib
import logging
import time
from google.appengine.ext import db
from models.user_model import *
from models.category_model import *
from models.blog_model import *

ancestor_key = db.Key.from_path('User', 'some_id')
# import memchache
from google.appengine.api import memcache
SECRET = "PYTHON"
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

# database stuffs
def get_posts(update = False) :
    """ 
        This obtain the post from the Cache. The Cache is always update
        and it get update when a user make a new Post. We only read in the
        Database when we write on it
    """
    # using the global variable query time
    key = "post"
    posts = memcache.get(key)
    if posts is None or update :
        logging.error("DBQUERY")
        # getting post from the database
        # posts = db.GqlQuery("SELECT  * FROM Blog order by date desc limit 10")
        posts = Blog.all().order("-date")
        posts.ancestor(ancestor_key)
        posts = list(posts)
        # saving the last time query to the database
        memcache.set("time_last_query", time.time()) 
        # updating cache
        memcache.set(key, posts)
    return posts

def get_category():
    """
        return all categories
    """
    return list(Category.all())

def post_by_category(category):
    """
        returns posts filter by one categorie
    """
    post = Blog.all().filter('category =', category.key())
    logging.error(post)
    return list(post)

# number of post by topic
def numpost_by_categories():
    """
        it returns a dictionary with the topics and its numbers of pos
    t"""
    topics = get_category()
    data = {}
    if topics :
        for topic in topics :
            post = post_by_category(topic)
            data[topic.name] = len(post)
        logging.error(data)
        return data
    else :
        return None

def get_permalink(post_id, update = False) :
    #cache reference memcache[postid] = [post, time]
    # create key from id
    key = db.Key.from_path('Blog', int(post_id), parent = ancestor_key)
    cache_key = str(key)
    # look for the post in the cache
    post = memcache.get(cache_key)
    if not post or update :
        logging.error("DBQUERY")
        # obtain the model from the key
        post = db.get(key)
        query_time = time.time()
        memcache.set(cache_key, [post, query_time])
    else :
        # if exists the post in the cache take it
        post = memcache.get(cache_key)[0]
    return post

# date to string
def date_to_string(date):
    return date.strftime('%a %b %m %X %Y')

