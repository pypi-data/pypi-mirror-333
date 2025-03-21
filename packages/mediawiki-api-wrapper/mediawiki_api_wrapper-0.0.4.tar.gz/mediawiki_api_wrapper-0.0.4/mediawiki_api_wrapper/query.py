import requests
import json
import datetime
import mediawiki_api_wrapper.retrying_connection as retrying_connection
import urllib.parse

def escape_parameter(parameter):
    return urllib.parse.quote(parameter.encode('utf8'))

def deletion_history(file, URL="https://wiki.openstreetmap.org/w/api.php"):
    # https://wiki.openstreetmap.org/w/api.php?action=query&list=logevents&lelimit=3&format=json&leaction=delete/delete&letitle=File:Wanderwegsymbol_Naturpark_Vorderer_Bayerischer_Wald.PNG
    # https://wiki.openstreetmap.org/w/api.php?action=query&list=logevents&lelimit=3&format=json&leaction=delete/delete&letitle=File:Wandearwegsymbol_Naturpark_Vorderer_Bayerischer_Wald.PNG
    url = URL + "?action=query&list=logevents&lelimit=3&format=json&leaction=delete/delete&letitle=" + escape_parameter(file) + "&prop=imageinfo&iilimit=50&format=json"
    response = retrying_connection.post(url, headers={'Content-type': 'text'})
    if "query" not in response.json():
        print(response.json())
    if 'error' in response.json():
        if 'invalidtitle' == response.json()['error']['code']:
            print("requested listing of deletion history of")
            print(file)
            print("on wiki")
            print(URL)
            print("This file name was listed as invalid")
        return None
    return response.json()["query"]["logevents"]

def file_upload_history(file, URL="https://wiki.openstreetmap.org/w/api.php", debug=False):
    """
    how it works with uploaded but deleted files?
    appears to be returning None
    https://wiki.openstreetmap.org/w/index.php?title=File:Video_OSM.png&action=edit&redlink=1
    print(mediawiki_api_query.file_upload_history("File:Video OSM.png"))
    """
    call_url = URL + "?action=query&titles=" + escape_parameter(file) + "&prop=imageinfo&iilimit=50&format=json"
    response = retrying_connection.post(call_url, headers={'Content-type': 'text'})
    if 'error' in response.json():
        print(response.json())
        raise
    if 'query' not in response.json():
        print(response.json())
    key = list(response.json()['query']['pages'].keys())[0]
    upload_history = response.json()['query']['pages'][key]
    if "imageinfo" not in upload_history:
        if debug:
            print(call_url)
            print(json.dumps(response.json(), indent=4))
            print(json.dumps(upload_history, indent=4))
        if 'query' not in upload_history:
            return None # https://wiki.openstreetmap.org/wiki/Talk:Wiki#Ghost_file - what is going on?
            raise Exception("unexpected missing query in data")
        if debug:
            print(json.dumps(upload_history['query']['pages'], indent=4))
            print(list(upload_history['query']['pages'].keys())[0])
    return upload_history["imageinfo"]

def file_upload_history_without_broken_uploads(file, URL="https://wiki.openstreetmap.org/w/api.php"):
    data = file_upload_history(file, URL)
    returned = []
    for entry in data:
        if "filemissing" not in entry:
            returned.append(entry)
    return returned

def debug_api():
    files = ["File:20170907 172429.jpg", "File:Global Relative Share Pie Chart.png"]
    for file in files:
        file = file.replace(" ", "%20")
        # versions of file itself
        url = "https://wiki.openstreetmap.org/w/api.php?action=query&titles=" + escape_parameter(file) + "&prop=imageinfo&iilimit=50&format=json"
        response = retrying_connection.post(url) # , data=data
        print(json.dumps(response.json(), indent=4))
        # versions of file page
        url = "https://wiki.openstreetmap.org/w/api.php?action=query&prop=revisions&titles=" + escape_parameter(file) + "&rvlimit=5&rvprop=timestamp|user|comment&format=json"
        response = retrying_connection.post(url) # , data=data
        print(response)
        print(json.dumps(response.json(), indent=4))
        print()
        print("00000000000000000000000000")
        print()

def all_pages(URL="https://wiki.openstreetmap.org/w/api.php"):
    # https://www.mediawiki.org/wiki/API:Allpages
    # https://www.mediawiki.org/w/api.php?action=query&list=allpages
    continue_parameter = "apcontinue"
    continue_code = None
    # https://wiki.openstreetmap.org/w/api.php?action=query&generator=categorymembers&gcmtitle=Category:Media%20without%20a%20license&prop=categories&cllimit=max&gcmlimit=max&format=json
    # https://wiki.openstreetmap.org/wiki/Category:Media_without_a_license_-_without_subcategory
    while True:
        url = URL + "?action=query&list=allpages&format=json"
        if continue_code != None:
            url += "&" + continue_parameter + "=" + continue_code
        print(url)
        print()
        response = retrying_connection.post(url)

        data = response.json()["query"]["allpages"]
        for entry in data:
            yield entry["title"]
        if "continue" in response.json():
            continue_code = response.json()["continue"][continue_parameter]
        else:
            break

def pages_from_category(category, URL="https://wiki.openstreetmap.org/w/api.php"):
    """
    category should be something like Category:name
    """
    continue_parameter = "gcmcontinue"
    continue_code = None
    # https://wiki.openstreetmap.org/w/api.php?action=query&generator=categorymembers&gcmtitle=Category:Media%20without%20a%20license&prop=categories&cllimit=max&gcmlimit=max&format=json
    # https://wiki.openstreetmap.org/wiki/Category:Media_without_a_license_-_without_subcategory
    while True:
        url = URL + "?action=query&generator=categorymembers&gcmtitle=" + escape_parameter(category) + "&gcmlimit=max&format=json"
        if continue_code != None:
            url += "&" + continue_parameter + "=" + continue_code
        print(url)
        print()
        response = retrying_connection.post(url)
        if 'error' in response.json():
            if 'invalidcategory' == response.json()['error']['code']:
                print("requested listing of pages in category")
                print(category)
                print("on wiki")
                print(URL)
                print("This category was listed as nonexisting")
                raise
        if 'error' in response.json():
            print(response.json())
            raise
        if "query" not in response.json():
            # empty
            # see for example
            # https://wiki.openstreetmap.org/w/api.php?action=query&generator=categorymembers&gcmtitle=Category%3AMaps%20of%20places%20in%20Antarctica&gcmlimit=max&format=json
            return []
        data = response.json()["query"]["pages"]
        keys = response.json()["query"]["pages"].keys()
        for key in keys:
            yield data[key]["title"]
        if "continue" in response.json():
            continue_code = response.json()["continue"][continue_parameter]
        else:
            break
    # https://stackoverflow.com/questions/28224312/mediawiki-api-how-do-i-list-all-pages-of-a-category-and-for-each-page-show-all

def uncategorized_images():
    group = 0
    while True:
        images = uncategorized_images_group(group * 500, 500)
        if len(images) == 0:
            return
        for image in images:
            yield image
        group += 1

def uncategorized_images_group(offset, how_many_in_group, URL="https://wiki.openstreetmap.org/w/api.php"):
    # example:
    # https://wiki.openstreetmap.org/w/api.php?action=query&format=json&list=querypage&utf8=1&qppage=Uncategorizedimages&qplimit=10&qpoffset=0
    url = URL + "?action=query&format=json&list=querypage&utf8=1&qppage=Uncategorizedimages&qplimit=" + str(how_many_in_group) + "&qpoffset=" + str(offset)
    response = retrying_connection.post(url)
    #print(json.dumps(response.json(), indent=4))
    file_list = response.json()['query']['querypage']['results']
    returned = []
    for file in file_list:
        returned.append(file["title"])
    return returned

def images_by_date(date_string):
    # https://www.mediawiki.org/wiki/API:Allimages#Example_2:_Get_images_by_date
    # "aistart The timestamp to start enumerating from. Can only be used with aisort=timestamp. "
    S = requests.Session()
    continue_code = None
    continue_parameter = "aicontinue"
    while True:
        URL = "https://wiki.openstreetmap.org/w/api.php"

        params = {
            "action": "query",
            "format": "json",
            "list": "allimages",
            "aisort": "timestamp",
            "aidir": "newer", # older
            "aistart": date_string,
            "ailimit": 500,
        }
        if continue_code != None:
            params[continue_parameter] = continue_code

        R = retrying_connection.get(URL, params=params, session=S)
        DATA = R.json()

        IMAGES = DATA["query"]["allimages"]

        returned = []
        for img in IMAGES:
            yield img["title"]
        if "continue" in DATA:
            continue_code = DATA["continue"][continue_parameter]
        else:
            break


class InvalidUsername(Exception):
   """Raised when mediawiki api claims that username is malformed"""

def uploads_by_username_generator(user, URL="https://wiki.openstreetmap.org/w/api.php"):
    continue_code = None
    continue_parameter = "aicontinue"
    # https://wiki.openstreetmap.org/w/api.php?action=query&list=allimages&aisort=timestamp&aiuser=Mateusz%20Konieczny
    while True:
        user = user.replace(" ", "%20")
        url = URL + "?action=query&list=allimages&aisort=timestamp&aiuser=" + user + "&format=json"
        if continue_code != None:
            url += "&" + continue_parameter + "=" + continue_code
        response = retrying_connection.post(url)
        #print(json.dumps(response.json(), indent=4))
        #print(url)
        if 'error' in response.json():
            if 'baduser' == response.json()['error']['code']:
                raise InvalidUsername(user + " claimed to be invalid username")
            print()
            print()
            print()
            print("---------------------")
            print(user)
            print(response.json())
            raise
        if 'query' not in response.json():
            print(response.json())
        file_list = response.json()['query']['allimages']
        returned = []
        for file in file_list:
            yield file["title"]
        if "continue" in response.json():
            #print(response.json()["continue"])
            continue_code = response.json()["continue"][continue_parameter]
        else:
            break

def download_page_text_with_revision_data(page_title, URL="https://wiki.openstreetmap.org/w/api.php"):
    if page_title == None:
        raise Exception("None passed as a title")
    # https://wiki.openstreetmap.org/w/api.php?action=query&prop=revisions&rvlimit=1&rvprop=content|timestamp|ids&format=json&titles=Sandbox
    url = URL + "?action=query&prop=revisions&rvlimit=1&rvprop=content|timestamp|ids&format=json&titles=" + escape_parameter(page_title)
    response = retrying_connection.post(url)
    if 'error' in response.json():
        print(response.json())
        raise
    if 'query' not in response.json():
        print(response.json())
    key = list(response.json()['query']['pages'].keys())[0]
    versions = response.json()['query']['pages'][key]
    if "revisions" not in versions:
        #print([page_title, "does not exist"])
        return None
    page_text = versions['revisions'][0]['*']
    rev_id = versions['revisions'][0]['revid']
    parent_id = versions['revisions'][0]['parentid']
    timestamp = versions['revisions'][0]['timestamp']
    return {'page_title': page_title, 'page_text': page_text, 'rev_id': rev_id, 'parent_id': parent_id, 'timestamp': timestamp}

def download_page_text(page_title, URL="https://wiki.openstreetmap.org/w/api.php"):
    url = URL + "?action=query&prop=revisions&rvlimit=1&rvprop=content&format=json&titles=" + escape_parameter(page_title)
    response = retrying_connection.post(url)
    #print(json.dumps(response.json(), indent=4))
    if 'error' in response.json():
        print(response.json())
        raise
    if 'query' not in response.json():
        print(response.json())
    key = list(response.json()['query']['pages'].keys())[0]
    versions = response.json()['query']['pages'][key]
    if "revisions" not in versions:
        print([page_title, "does not exist"])
        return None
    page_text = versions['revisions'][0]['*']
    #print(page_text)
    return page_text

def is_used_as_image_anywhere(page_title, URL="https://wiki.openstreetmap.org/w/api.php"):
    for page_title in pages_where_file_is_used_as_image(page_title, URL):
        return True
    return False

def pages_where_file_is_used_as_image(page_title, URL="https://wiki.openstreetmap.org/w/api.php"):
    continue_code = None
    continue_parameter = "fucontinue"
    # https://wiki.openstreetmap.org/w/api.php?action=query&list=allimages&aisort=timestamp&aiuser=Mateusz%20Konieczny
    while True:
        # https://wiki.openstreetmap.org/w/api.php?action=query&titles=File:Canopy-action.jpg&prop=fileusage&format=json
        url = URL + "?action=query&titles=" + escape_parameter(page_title) + "&prop=fileusage&format=json"
        if continue_code != None:
            url += "&" + continue_parameter + "=" + continue_code
        response = retrying_connection.post(url)
        if 'error' in response.json():
            print(response.json())
            raise
        if 'query' not in response.json():
            print(response.json())
        key = list(response.json()['query']['pages'].keys())[0]
        entry = response.json()['query']['pages'][key]
        if "fileusage" not in entry:
            break
        else:
            for use in entry["fileusage"]:
                yield use["title"]
        if "continue" in response.json():
            #print(response.json()["continue"])
            continue_code = response.json()["continue"][continue_parameter]
        else:
            break

def is_file_used_as_image(page_title, URL="https://wiki.openstreetmap.org/w/api.php"):
    url = URL + "?action=query&titles=" + escape_parameter(page_title) + "&prop=fileusage&format=json"
    response = retrying_connection.post(url)
    #print(json.dumps(response.json(), indent=4))
    if 'error' in response.json():
        print(response.json())
        raise
    if 'query' not in response.json():
        print(response.json())
    key = list(response.json()['query']['pages'].keys())[0]
    #print("-=--------------")
    #print(json.dumps(response.json(), indent=4))
    #print("-=--------------")
    entry = response.json()['query']['pages'][key]
    return "fileusage" in entry

    # backlinks: https://wiki.openstreetmap.org/w/api.php?action=query&format=json&list=backlinks&bltitle=File:01.Picture.jpg

def get_uploader(page_title):
    """
    returns uploader username
    or returns None if different versions were uploaded by a different people
    """
    upload_history = file_upload_history(page_title)
    return get_uploader_from_file_history(upload_history)

def get_uploader_from_file_history(upload_history):
    #print()
    #print("------------------------")
    #print(upload_history)
    #print(len(upload_history))
    #print("------------------------")
    #print("----UPLOAD HISTORY------")
    #print("------------------------")
    #print()
    
    user = upload_history[0]['user']

    for entry in upload_history:
        # upload_history:
        # [{'timestamp': '2011-02-15T11:26:49Z', 'user': 'Say-no'}, {'filemissing': ''}]
        # entry:
        # {'filemissing': ''}
        if 'filemissing' in entry:
            continue
        if "user" not in entry:
            print("upload_history:", upload_history)
            print("len(upload_history):", len(upload_history))
        if user != entry['user']:
            print("multiple uploads by different people, lets skip for now as complicated")
            return None
    return user

def get_upload_date_from_file_history(upload_history):
    if(len(upload_history) > 1):
        print("multiple uploads, lets skip obtaining upload date for now as complicated")
        return None
    return get_the_first_upload_date_from_file_history(upload_history)

def get_the_first_upload_date_from_file_history(upload_history):
    upload_timestamp_string = upload_history[-1]['timestamp']
    return parse_mediawiki_time_string(upload_timestamp_string)

def parse_mediawiki_time_string(time_string):
    return datetime.datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%SZ")
