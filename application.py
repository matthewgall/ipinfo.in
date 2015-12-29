#!/usr/bin/env python

import os
import json
import socket
import logging
from bottle import route, request, response, error, hook, default_app
from logentries import LogentriesHandler
from dicttoxml import dicttoxml
from IPy import IP
import pydenticon

def get_ipaddress():
    """Return the IP address of the visitor to the calling function."""
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
    """Return the reverse hostname of the IP address to the calling function."""
    try:
        return socket.gethostbyaddr(get_ipaddress())[0]
    except:
        return "Unable to resolve IP address to reverse hostname"

def get_request_headers():
    """Return an array of headers used to make the request to the calling function."""
    return request.headers.keys()

@hook('after_request')
def add_headers():
    """Added a set of headers to all responses from the application."""
    response.set_header('X-Contact', 'themaster@ipinfo.in')

def build_content_response(content):
    """Builds a content response."""
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
    response.content_type = 'image/png'
    address = IP(get_ipaddress())
    values = []
    if address.version() == 6:
        address = str(address).split(":")
        for ochet in address:
            if ochet == '':
                values.append("0")
            elif int(ochet) >= 255:
                values.append("255")
            else:
                values.append(ochet)
    else:
        address = str(address).split(".")
        for ochet in address:
            values.append(ochet)

    colors = []
    colors.append("rgb(" + values[0] \
        + "," + values[1] \
        + "," + values[2] + ")")
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
            content = content + "<strong>" + key + "</strong>: " \
                + str(request.headers.get(key)) + "</br>"
        response.content_type = 'text/html'
        return content

@route('/reverse')
@route('/reverse.json')
@route('/reverse.xml')
def reverse():
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

    app = default_app()

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
        app.run(host=serverHost, port=serverPort)
    except:
        log.info("Failed to start application server on " + socket.gethostname())
