import mediawiki_api_wrapper.query as query
import webbrowser
import urllib

def show_latest_diff_on_page(page_title):
    if page_title == None:
        raise Exception("None passed as a title")
    data = query.download_page_text_with_revision_data(page_title)
    difflink = osm_wiki_diff_link(data['parent_id'], data['rev_id'])
    webbrowser.open(difflink, new=2)

def osm_wiki_diff_link(old_page_id, current_page_id):
    url = "https://wiki.openstreetmap.org/wiki/?diff=" + str(current_page_id) + "&oldid=" + str(old_page_id)
    return url

def osm_wiki_page_link(page_name):
    url = "https://wiki.openstreetmap.org/wiki/" + escape_parameter(page_name)
    url = url.replace(" ", "_")
    return url

def osm_wiki_page_edit_link(page_name):
    url = "https://wiki.openstreetmap.org/wiki?title=" + escape_parameter(page_name) + "&action=edit"
    url = url.replace(" ", "_")
    return url

def escape_parameter(parameter):
    return urllib.parse.quote(parameter.encode('utf8'))
