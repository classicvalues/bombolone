# -*- coding: utf-8 -*-
"""
login.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
import re
import httplib
import oauth.oauth as oauth
from flask import request, session, g, render_template, url_for, redirect, Markup, abort
from time import time

# Imports inside Bombolone
import model.users
from config import PATH, PATH_API, NOTACTIVATED
from core.utils import create_password

def sign_in(username_or_email=None,
            password=None,
            permanent=None):
    """
    Sign the user in.
    We check the user by both the username or email. 

    """
    error_code = None

    if not username_or_email or not password:
        error_code = ('login_msg', 'login_error_1')

    if not error_code:
        user = model.users.find(username=username_or_email, only_one=True, my_rank=10)

        if user is None:
            user = model.users.find(email=username_or_email, only_one=True, my_rank=10)

        if user is None:
            error_code = ('login_msg', 'login_error_2')

        if not error_code and user["status"] == NOTACTIVATED:
            error_code = ('login_msg', 'login_error_3')

        elif not error_code and not user['password'] == create_password(password):
            error_code = ('login_msg', 'login_error_2')

        if not error_code:
            model.users.update(user_id=user["_id"])
            if permanent is not None:
                permanent = True
            return {
                "success": True,
                "user_id": str(user['_id']),
                "permanent": permanent
            }
    return dict(success=False, errors=[{ "code": error_code }])

def core_logout(token):
    """
    Remove the given token from oauth_tokens

    :param token: the token to remove
    """
    model.oauth_tokens.remove(token)
