import urllib2
import json


def login(username, password, base_url, login_url):

    url_login = base_url + login_url

    data = {"username" : username,
    "password" : password,
    "scope" : "web portal"
    }

    request = urllib2.Request(url_login, json.dumps(data))
    request.add_header('Content-Type', 'application/json')
    json_url = urllib2.urlopen(request)
    response = json.loads(json_url.read())

    token = response['token']['authToken']
    user_id = response['user']['id']

    return {'token': token, 'id': user_id, 'username': username}


def logout(user, base_url, logout_url):

    url_logout = base_url + logout_url

    data = {'authToken': user['token']}

    request = urllib2.Request(url_logout, json.dumps(data))
    request.add_header('Content-Type', 'application/json')
    json_url = urllib2.urlopen(request)
    response = json.loads(json_url.read())

    if response['code'] <= 204:
        print "Logged out %s" % user['username']
    else:
        print "Logging out error %s : %s" % (response['code'], response['error'])
        print response['devmsg']
