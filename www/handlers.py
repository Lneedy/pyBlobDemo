#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'lneedy'

' url handlers  routers'

from coroweb import get, post
import re, time, json, logging, hashlib, base64, asyncio
from apiDefind import APIValueError, APIError, APIResourceNotFoundError
from aiohttp import web
from models import User, Blog, Comment, next_id
from config import configs
_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')
COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

def user2cookie (user, max_age):
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

async def cookie2user(cookie_str):
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = await User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invaild sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None

@get('/')
def index(request):
    logging.info('index...')
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, created_at=time.time() - 120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time() - 3600),
        Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time() - 7200)
    ]
    return {
        '__template__': 'blog.html',
        'blogs': blogs
    }

@get('/blog')
async def blog(request):
    users = await User.findAll()
    return {
        '__template__': 'blog.html',
        'users': users
    }

@get('/register')
async def register(request):
    return {
        '__template__': 'register.html'
    }


# @get('/api/users')
# async def api_get_users(*, page='1'):
#     users = await User.findAll(orderBy='created_at desc')
#     for u in users:
#         u.passwd = '******'
#     return dict(user=users)

@post('/api/users')
async def api_register_user(*, email, name, passwd):
    logging.info('api:users...')
    if not name or not name.strip():
        raise APIValueError('name')
    logging.info('api:users1...')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    logging.info('api:users11...')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    logging.info('api:users111...')
    users = await User.findAll('email=?', [email])
    logging.info('api:users1111...')
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    await user.save()
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r