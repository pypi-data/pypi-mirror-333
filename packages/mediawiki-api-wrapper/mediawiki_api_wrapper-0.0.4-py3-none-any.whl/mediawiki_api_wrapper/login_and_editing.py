#!/usr/bin/python3

import requests
import simplejson
import mediawiki_api_wrapper.retrying_connection as retrying_connection
import mediawiki_api_wrapper.query as query
import mediawiki_api_wrapper.interface as interface
import time

class NoEditPermissionException(Exception):
   # likely logged out
   pass

"""
    login.py

    MediaWiki API Demos
    Demo of `Login` module: Sending post request to login
    MIT license
    https://www.mediawiki.org/wiki/API:Login#Python
    https://wiki.openstreetmap.org/wiki/Special:BotPasswords
"""
def login_and_create_session(username, password, URL="https://wiki.openstreetmap.org/w/api.php"):
    S = requests.Session()
    LOGIN_TOKEN = obtain_login_token(S, URL)

    # Send a post request to login. Using the main account for login is not
    # supported. Obtain credentials via Special:BotPasswords
    # (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword

    return login_with_login_token(S, username, password, LOGIN_TOKEN, URL)

def login_with_login_token(S, username, password, LOGIN_TOKEN, URL):
    PARAMS_1 = {
        'action':"login",
        'lgname': username,
        'lgpassword': password,
        'lgtoken':LOGIN_TOKEN,
        'format':"json"
    }

    R = retrying_connection.post(URL, PARAMS_1, session=S)
    DATA = R.json()
    # TODO - handle failure?
    if is_error_here(DATA):
        raise
    return S

def is_rate_limit_error_here(DATA):
    #{'error': {'code': 'ratelimited', 'info': 'As an anti-abuse measure, you are limited from performing this action too many times in a short space of time, and you have exceeded this limit. Please try again in a few minutes.', '*': 'See https://wiki.openstreetmap.org/w/api.php for API usage. Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/mailman/listinfo/mediawiki-api-announce&gt; for notice of API deprecations and breaking changes.'}}
    if 'error' in DATA:
        if DATA['error']['code'] == 'ratelimited':
            return True
    return False

def is_logged_out_error_here(DATA):
    #{'error': {'code': 'permissiondenied', 'info': 'The action you have requested is limited to users in the group: [[Wiki:Users|Users]].' ...
    # triggered by attempting to edit
    #
    # notloggedin is triggered when attempting to watchlist
    if 'error' in DATA:
        if DATA['error']['code'] in ['notloggedin', 'permissiondenied']:
            return True
    return False

def is_error_here(DATA):
    if 'error' in DATA:
        return True
    return False


def create_page(S, page_title, page_text, edit_summary, URL="https://wiki.openstreetmap.org/w/api.php", sleep_time=0.4, mark_as_bot_edit=False):
    # Step 4: POST request to edit a page
    params = {
        "action": "edit",
        "title": page_title,
        "token": obtain_csrf_token(S, URL),
        "format": "json",
        "text": page_text,
        "summary": edit_summary,
        "createonly": "1",
    }
    if mark_as_bot_edit:
        params["bot"] = "yes"

    R = retrying_connection.post(URL, params, session=S)
    DATA = R.json()

    print(DATA)
    if is_logged_out_error_here(DATA):
        raise NoEditPermissionException("likely automatically logged out")
    if is_rate_limit_error_here(DATA):
        print("rate limit error, will retry after sleeeping")
        time.sleep(60)
        print("rate limit error, sleep finished, will retry")
        create_page(S, page_title, page_text, edit_summary, URL)
    elif is_error_here(DATA):
        raise
    time.sleep(sleep_time)

def edit_page(S, page_title, page_text, edit_summary, rev_id, timestamp, URL="https://wiki.openstreetmap.org/w/api.php", sleep_time=0.4, mark_as_bot_edit=False):
    try:
        # https://www.mediawiki.org/wiki/API:Edit
        # Step 4: POST request to edit a page
        params = {
            "action": "edit",
            "title": page_title,
            "token": obtain_csrf_token(S, URL),
            "format": "json",
            "text": page_text,
            "summary": edit_summary,
            "baserevid": rev_id,
            "basetimestamp": timestamp,
            "nocreate": "1",
        }
        if mark_as_bot_edit:
            print("Marking as bot edit")
            params["bot"] = "yes"
        else:
            print("Not marking as bot edit")

        R = retrying_connection.post(URL, params, session=S)
        DATA = R.json()
        print(DATA)
        if is_logged_out_error_here(DATA):
            raise NoEditPermissionException("likely automatically logged out")
        if is_rate_limit_error_here(DATA):
            print("rate limit error, will retry after sleeeping")
            time.sleep(60)
            print("rate limit error, sleep finished, will retry")
            edit_page(S, page_title, page_text, edit_summary, rev_id, timestamp, URL, sleep_time=sleep_time, mark_as_bot_edit=mark_as_bot_edit)
        elif is_error_here(DATA):
            if DATA['error']['code'] == 'abusefilter-disallowed':
                # OSM Wiki error
                if DATA['error']['abusefilter']['description'] == 'Adding literal characters outside the Basic Multilingual Plane':
                    print('Adding literal characters outside the Basic Multilingual Plane')
                    print(page_text)
            raise
        time.sleep(sleep_time)
    except requests.exceptions.MissingSchema as e:
        print()
        print()
        print("----------------------------------")
        print("edit_page - encountered requests.exceptions.MissingSchema")
        print("session:", S, "page_title:", page_title, "edit_summary:", edit_summary, "rev_id:", rev_id, "timestamp:", timestamp, "URL:", URL, "sleep_time:", sleep_time, "mark_as_bot_edit:", mark_as_bot_edit)
        print("------------")
        print("page_text:", page_text)
        print("----------------------------------")
        raise


def watchlist_page(S, page_title, URL="https://wiki.openstreetmap.org/w/api.php"):
    # https://www.mediawiki.org/wiki/API:Watch

    PARAMS_FOR_TOKEN = {
        "action": "query",
        "meta": "tokens",
        "type": "watch",
        "format": "json"
    }
    R = retrying_connection.get(URL, params=PARAMS_FOR_TOKEN, session=S)
    DATA = R.json()
    CSRF_TOKEN = DATA["query"]["tokens"]["watchtoken"]

    PARAMS = {
        "action": "watch",
        "titles": page_title,
        "format": "json",
        "token": CSRF_TOKEN,
    }

    R = retrying_connection.post(URL, PARAMS, session=S)
    DATA = R.json()
    if is_logged_out_error_here(DATA):
        raise NoEditPermissionException("likely automatically logged out")
    elif is_error_here(DATA):
        print(R)
        print(R.status_code)
        print(R.content)
        print(R.text)
        raise
    if is_error_here(DATA):
        raise

def obtain_csrf_token(S, URL):
    try:
        # CSRF == Cross Site Request Forgery
        # AKA, additional complexity because some people are evil

        # GET request to fetch CSRF token
        PARAMS = {
            "action": "query",
            "meta": "tokens",
            "format": "json"
        }

        R = retrying_connection.get(URL, params=PARAMS, session=S)
        DATA = R.json()
        if is_error_here(DATA):
            raise
        CSRF_TOKEN = DATA['query']['tokens']['csrftoken']
        return CSRF_TOKEN
    except simplejson.errors.JSONDecodeError:
        print(R)
        print(R.status_code)
        print(R.content)
        print(R.text)
        raise
    except requests.exceptions.ConnectionError as e:
        print("ERROR HAPPENED")
        print(e)
        time.sleep(120)
        return obtain_csrf_token(S, URL)
    except requests.exceptions.MissingSchema as e:
        print()
        print()
        print("----------------------------------")
        print("obtain_csrf_token - encountered requests.exceptions.MissingSchema")
        print("obtain_csrf_token - URL", URL)
        print("----------------------------------")
        raise

def obtain_login_token(S, URL):
    # Retrieve login token first
    PARAMS_0 = {
        'action':"query",
        'meta':"tokens",
        'type':"login",
        'format':"json"
    }

    #R = S.get(url=URL, params=PARAMS_0, timeout=120)
    R = retrying_connection.get(URL, params=PARAMS_0, session=S)
    try:
        DATA = R.json()
        if is_error_here(DATA):
            raise
        LOGIN_TOKEN = DATA['query']['tokens']['logintoken']
        return LOGIN_TOKEN
    except simplejson.errors.JSONDecodeError:
        print(R)
        print(R.status_code)
        print(R.content)
        print(R.text)
        raise Exception("JSON decoding failed while obtaining login token")
        

def edit_page_and_show_diff(session, page_title, page_text, edit_summary, rev_id, timestamp, sleep_time = None, mark_as_bot_edit=False):
    try:
        if sleep_time != None:
            returned = edit_page(session, page_title, page_text, edit_summary, rev_id, timestamp, sleep_time=sleep_time, mark_as_bot_edit=mark_as_bot_edit)
        returned = edit_page(session, page_title, page_text, edit_summary, rev_id, timestamp, mark_as_bot_edit=mark_as_bot_edit)
        interface.show_latest_diff_on_page(page_title)
        return returned
    except requests.exceptions.MissingSchema as e:
        print()
        print()
        print("----------------------------------")
        print("edit_page_and_show_diff - encountered requests.exceptions.MissingSchema")
        print("session:", session, "page_title:", page_title, "edit_summary:", edit_summary, "rev_id:", rev_id, "timestamp:", timestamp, "sleep_time:", sleep_time, "mark_as_bot_edit:", mark_as_bot_edit)
        print("------------")
        print("page_text:", page_text)
        print("----------------------------------")
        raise

def create_page_and_show_diff(session, page_title, page_text, edit_summary, sleep_time = None, mark_as_bot_edit=False):
    returned = None
    if sleep_time != None:
        returned = create_page(session, page_title, page_text, edit_summary, sleep_time=sleep_time, mark_as_bot_edit=mark_as_bot_edit)
    else:
        returned = create_page(session, page_title, page_text, edit_summary, mark_as_bot_edit=mark_as_bot_edit)
    interface.show_latest_diff_on_page(page_title)
    return returned

def replace_text_on_page(session, page_title, page_text, edit_summary, sleep_time = None, mark_as_bot_edit=False):
    page_data = query.download_page_text_with_revision_data(page_title)
    if page_data != None:
        edit_page(session, page_title, page_text, edit_summary, page_data['rev_id'], page_data['timestamp'], mark_as_bot_edit=mark_as_bot_edit)
    else:
        create_page(session, page_title, page_text, edit_summary, mark_as_bot_edit=mark_as_bot_edit)

def replace_text_on_page_and_show_diff(session, page_title, page_text, edit_summary, sleep_time = None, mark_as_bot_edit=False):
    page_data = query.download_page_text_with_revision_data(page_title)
    if page_data != None:
        edit_page_and_show_diff(session, page_title, page_text, edit_summary, page_data['rev_id'], page_data['timestamp'], mark_as_bot_edit=mark_as_bot_edit)
    else:
        create_page_and_show_diff(session, page_title, page_text, edit_summary, mark_as_bot_edit=mark_as_bot_edit)


def append_text_to_page_and_show_diff(session, page_title, appended_text, edit_summary, sleep_time = None, mark_as_bot_edit=False):
    page_data = query.download_page_text_with_revision_data(page_title)
    page_text = ""
    if page_data != None:
        page_text = page_data['page_text'] + appended_text
        edit_page_and_show_diff(session, page_title, page_text, edit_summary, page_data['rev_id'], page_data['timestamp'], mark_as_bot_edit=mark_as_bot_edit)
    else:
        page_text = appended_text
        create_page_and_show_diff(session, page_title, page_text, edit_summary, mark_as_bot_edit=mark_as_bot_edit)


def append_text_to_page(session, page_title, appended, edit_summary):
    data = query.download_page_text_with_revision_data(page_title)
    page_text = data['page_text'] + appended
    returned = edit_page_and_show_diff(session, page_title, page_text, edit_summary, data['rev_id'], data['timestamp'])
    return returned

def null_edit(session, page_title):
    test_page = query.download_page_text_with_revision_data(page_title)
    text = test_page['page_text']
    edit_page(session, page_title, text, "NULL EDIT", test_page['rev_id'], test_page['timestamp'])
