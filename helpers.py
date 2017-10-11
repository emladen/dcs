'''
Created on Oct 2, 2017

@author: root
'''

import web
import sqlite3
import random
import sys
from sqlite3 import Error
from hashlib import sha512
import bcrypt
from bcrypt import hashpw, gensalt

import pprp
import base64

from web.webapi import seeother
from web import form

g_user = 'admin'
g_password = 'admin'
g_pepper = '3gih8s8b8pmg'
g_key = '33mbv8m8g8a'
db_file = 'dcs.db'

create_user_table_sql = """CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY, 
                            user VARCHAR(50) NOT NULL UNIQUE, 
                            password VARCHAR(200), 
                            salt VARCHAR(80)
                            );"""

class PasswordHash(object):
    def __init__(self, password_):
        self.salt = "".join(chr(random.randint(33,127)) for x in xrange(64))
        self.saltedpw = sha512(password_ + self.salt).hexdigest()
    def check_password(self, password_):
        """checks if the password is correct"""
        return self.saltedpw == sha512(password_ + self.salt).hexdigest()



KEY_SIZE = 16
BLOCK_SIZE = 32


def encrypt(key, plaintext):
    key = key.encode('ascii')
    plaintext = plaintext.encode('utf-8')
    padded_key = key.ljust(KEY_SIZE, b'\0')

    sg = pprp.data_source_gen(plaintext, block_size=BLOCK_SIZE)
    eg = pprp.rjindael_encrypt_gen(padded_key, sg, block_size=BLOCK_SIZE)

    ciphertext = pprp.encrypt_sink(eg)

    encoded = base64.b64encode(ciphertext)

    return encoded.decode('ascii')


def decrypt(key, encoded):
    key = key.encode('ascii')
    padded_key = key.ljust(KEY_SIZE, b'\0')

    ciphertext = base64.b64decode(encoded.encode('ascii'))

    sg = pprp.data_source_gen(ciphertext, block_size=BLOCK_SIZE)
    dg = pprp.rjindael_decrypt_gen(padded_key, sg, block_size=BLOCK_SIZE)

    return pprp.decrypt_sink(dg).decode('utf-8')

def create_salt():
    return "".join(chr(random.randint(33,127)) for x in xrange(64))
    #for bcrpyt
    #return bcrypt.gensalt()

def create_saltedpw(password, salt):
    
    return sha512(password + g_pepper + salt).hexdigest()
    #return hashpw(password + g_pepper, salt)
    #for bcrypt
    #return hashpw(password, salt)

def create_db_connection(db_file):
    try:
        db_connect = sqlite3.connect('dcs.db')
        return db_connect
    except Error:
        print("Database connection Error")
    
    return None

def validate_user(conn, user, password):
    cur = conn.cursor()
    sql = "SELECT password, salt FROM users WHERE user=?"
    cur.execute("Select * From users WHERE user='admin'")
    cur.execute(sql, (user,))
    user_pw_s = cur.fetchall()
    if len(user_pw_s) > 0:
        d_salt = decrypt(g_key, user_pw_s[0][1])
        d_password = decrypt(g_key, user_pw_s[0][0])
        password = str(password).encode('utf-8')
        de_salt = str(d_salt).encode('utf-8')
        hash = create_saltedpw(password, de_salt)
        if hash == decrypt(g_key,user_pw_s[0][0]):
            return True
    return False

def create_table_if_not_exists(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error:
        print("Database execute Error")

def insert_value(conn, sql, record):
    try:
        cur = conn.cursor()
        cur.execute(sql,record)
    except Error as e:
        print ("An error occurred: " + e.args[0])
        print("Error! Cannot write to database.")

def is_user_table_empty(conn):
    cur = conn.cursor()
    cur.execute("Select * From users")
    rows = cur.fetchall()
    
    if len(rows) > 0:
        return False
    else:
        return True
    
def add_default_user(conn):
    cur = conn.cursor()
    sql = "INSERT INTO users (user,password,salt) VALUES (?, ?, ?)"
    salt = create_salt()
    password = create_saltedpw(g_password, salt)
    encrypted_pw = encrypt(g_key, password)
    encrypted_salt = encrypt(g_key, salt)
    
    cur.execute(sql, [g_user, encrypted_pw, encrypted_salt])
    conn.commit()


def setup_database():
    #try:
    try:
        conn = create_db_connection(db_file)
        with conn:
            create_table_if_not_exists(conn, create_user_table_sql)
            if is_user_table_empty(conn):
                add_default_user(conn)
    except Error as e:
        print("Error: " + e.args[0])
        sys.exit(1)
#         conn = create_db_connection(db_file)
#         if conn is not None:
#             create_table_if_not_exists(conn, create_user_table_sql)
#             if is_user_table_empty(conn):
#                 add_default_user(conn)
#             conn.close()
#         else:
#             print("Error! cannot create the database connection.")
    #except Error as e:
        #print("error" + e.args[0])
        #sys.exit(1)

def check_login(redirect=False):
    """
    Check login.
    """
    qdict = web.input()
    
    try:
#         if gv.sd['ipas'] == 1:
#             return True
    
        if web.config._session['user'] == 'admin':
            return True
    except KeyError:
        pass
    
    if ('password' in qdict) and ('username' in qdict):
        if validate_login(qdict['username'], qdict['password']):
            return True
        if redirect:
            raise web.unauthorized()
        return False
    
    
#     if 'pw' in qdict:
#         if gv.sd['password'] == password_hash(qdict['pw'], gv.sd['salt']):
#             return True
#         if redirect:
#             raise web.unauthorized()
#         return False
    
    if redirect:
        raise web.seeother('/login')
    return False

def validate_login(user, password):
    #return (user, password) [user == g_user and password == g_password]
    conn = create_db_connection(db_file)
    with conn:
        if validate_user(conn, user, password):
            return True
        else:
            return False
        
    if user == g_user and password == g_password:
        return True
    else:
        return False

def toogle_power_status(status):
    if status == "power-off":
        return "power-on"
    else:
        return "power-off"
