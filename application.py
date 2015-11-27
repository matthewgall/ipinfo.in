#!/usr/bin/env python

import os
import json
import socket
import logging
from random import randint
from bottle import route, request, response, run, error, default_app
from logentries import LogentriesHandler
from dicttoxml import dicttoxml
import pydenticon

def get_ipaddress():
    try:
        if request.headers.get('Cf-Connecting-Ip') == None \
        and request.headers.get('X-Forwarded-For') == None:
            raise TypeError
        elif request.headers.get('Cf-Connecting-Ip') != None:
            return request.headers.get('Cf-Connecting-Ip')
        else:
            return request.headers.get('X-Forwarded-For')
    except TypeError:
        return request.get('REMOTE_ADDR')

def get_reverse_host():
    try:
        return socket.gethostbyaddr(get_ipaddress())[0]
    except:
        return "Unable to resolve IP address to reverse hostname"
    
def get_request_headers():
    return request.headers.keys()

def add_headers():
    response.set_header('X-ContactTheAuthor', 'themaster@ipinfo.in')
    return True

def build_content_response(content):
    # First, we're going to add our headers as needed
    add_headers()
    # And define a default dictionary
    content = {
        "results": ""
    }
    return content

def is_json_response():
    if request.headers.get('Accept') == "application/json" \
    or request.path.endswith('.json'):
        response.content_type = 'application/json'
        return True

def is_xml_response():
    if request.headers.get('Accept') == "application/xml" \
    or request.path.endswith('.xml'):
        response.content_type = 'application/xml'
        return True

@route('favicon.ico')
@error(404)
def error_404(error):
    response.status = 404
    response.content_type = 'text/plain'
    return 'Nothing here, sorry'

@route('/version')
def get_version():
    add_headers()
    try:
        dirname, filename = os.path.split(os.path.abspath(__file__))
        del filename
        f = open(os.getenv('VERSION_PATH', dirname + '/.git/refs/heads/master'), 'r')
        content = f.read()
        response.content_type = 'text/plain'
        return content
    except:
        return "Unable to open version file."

@route('/icon')
@route('/icon/<height:int>')
@route('/icon/<height:int>/<width:int>')
def get_icon(height=100, width=100):
    add_headers()
    response.content_type = 'image/png'
    colors = []
    colors.append("rgb(" + str(randint(1, 255)) \
        + "," + str(randint(1, 255)) \
        + "," + str(randint(1, 255)) + ")")
    generator = pydenticon.Generator(8, 8, foreground=colors)
    identicon = generator.generate(get_ipaddress(), height, width)
    return identicon

@route('/headers')
@route('/headers.json')
@route('/headers.xml')
def headers():
    content = {
        "results": {}
    }
    for key in get_request_headers():
        content["results"][key] = request.headers.get(key)
    if is_json_response():
        return json.dumps(content)
    if is_xml_response():
        return dicttoxml(content)
    else:
        content = ""
        for key in get_request_headers():
            content = content + "<strong>" + key + "</strong>: " + str(request.headers.get(key)) + "</br>"
        response.content_type = 'text/html'
        return content

@route('/reverse')
@route('/reverse.json')
@route('/reverse.xml')
def reverse():
    add_headers()
    content = {
        "results": {
            'reverse': get_reverse_host()
        }
    }
    if is_json_response():
        return json.dumps(content)
    elif is_xml_response():
        return dicttoxml(content)
    else:
        response.content_type = 'text/plain'
        return get_reverse_host()

@route('/')
@route('/ip')
@route('/ip.json')
@route('/ip.xml')
def ip():
    add_headers()
    content = {
        "results": {
            'ip': get_ipaddress()
        }
    }
    if is_json_response():
        return json.dumps(content)
    elif is_xml_response():
        return dicttoxml(content)
    else:
        response.content_type = 'text/plain'
        return get_ipaddress()

if __name__ == '__main__':

    application = default_app()

    serverHost = os.getenv('SERVER_HOST', 'localhost')
    serverPort = os.getenv('SERVER_PORT', '5000')

    # Now we're ready, so start the server
    # Instantiate the logger
    log = logging.getLogger('log')
    console = logging.StreamHandler()
    log.setLevel(logging.INFO)
    log.addHandler(console)

    if os.getenv('LOGENTRIES_TOKEN') == '':
        log.addHandler(LogentriesHandler(os.getenv('LOGENTRIES_TOKEN', '')))

    # Now we're ready, so start the server
    try:
        log.info("Successfully started application server on " + socket.gethostname())
        application.run(host=serverHost, port=serverPort)
    except:
        log.info("Failed to start application server on " + socket.gethostname())
