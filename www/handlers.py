#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'lneedy'

' url handlers  routers'

from coroweb import get, post

import logging

from models import User, Blog, Comment, next_id

@get('/')
async def index(request):
    users = await User.findAll()
    return {
        '__template__': 'index.html',
        'users': users
    }

@get('/blog')
async def index(request):
    users = await User.findAll()
    return {
        '__template__': 'blog.html',
        'users': users
    }
