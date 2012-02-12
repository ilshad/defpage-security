import json
import base64
import httplib2
from pyramid.httpexceptions import HTTPUnauthorized
from defpage.lib.exceptions import ServiceCallError
from defpage.security.config import system_params

def _call(userid, url, method, body=None, headers={}):
    h = httplib2.Http()
    headers.update({"Authorization":"Basic " + base64.b64encode(str(userid or "") + ":1")})
    r, c = h.request(system_params.meta_url + url, method=method, body=body, headers=headers)
    if r.status == 401 or r.status == 403:
        raise HTTPUnauthorized
    return r, c

def search_collections(userid):
    r,c = _call(userid, "/collections/?user_id=" + str(userid), "GET", None)
    if r.status == 200:
        return json.loads(c)
    elif r.status == 400:
        return []
    raise ServiceCallError
