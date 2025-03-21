import requests
import time

def get(url, params={}, headers=None, session=None):
    try:
        response = None
        if headers != None:
            if session == None:
                response = requests.get(url=url, params=params, headers=headers, timeout=120)
            else:
                response = session.get(url=url, params=params, headers=headers, timeout=120)
        else:
            if session == None:
                response = requests.get(url=url, params=params, timeout=120)
            else:
                response = session.get(url=url, params=params, timeout=120)
        if response.status_code != 200:
            print("Warning! response.status_code:", response.status_code, "- will retry")
            return get(url, params, headers, session)
        return response
    except requests.exceptions.ConnectionError as e:
        print("requests.exceptions.ConnectionError")
        print(e)
        print(session)
        print(url)
        print(params)
        print(headers)
        sleep_time = 60
        print("sleeping for", sleep_time, "seconds and retrying, not sure about error source")
        time.sleep(sleep_time)
        return get(url, params, headers, session)
    except requests.exceptions.ReadTimeout as e:
        print(requests.exceptions.ReadTimeout)
        time.sleep(60)
        return get(url, params, headers, session)
    except requests.exceptions.MissingSchema as e:
        print()
        print()
        print("retying_connection.get - encountered requests.exceptions.MissingSchema")
        print("url", url)
        print("params", params)
        print("headers", headers)
        raise
        
    raise "impossible"

def post(url, params={}, headers=None, session=None):
    try:
        response = None
        if headers != None:
            if session == None:
                response = requests.post(url=url, data=params, headers=headers, timeout=120)
            else:
                response = session.post(url=url, data=params, headers=headers, timeout=120)
        else:
            if session == None:
                response = requests.post(url=url, data=params, timeout=120)
            else:
                response = session.post(url=url, data=params, timeout=120)
        if response.status_code != 200:
            print("Warning! response.status_code:", response.status_code, "- will retry")
            return post(url, params, headers, session)
        return response
    except requests.exceptions.ConnectionError as e:
        print("requests.exceptions.ConnectionError")
        print(e)
        print(session)
        print(url)
        print(params)
        print(headers)
        sleep_time = 60
        print("sleeping for", sleep_time, "seconds and retrying, not sure about error source")
        time.sleep(sleep_time)
        return post(url, params, headers, session)
    except requests.exceptions.ReadTimeout as e:
        print(requests.exceptions.ReadTimeout)
        time.sleep(60)
        return post(url, params, headers, session)
    raise "impossible"

