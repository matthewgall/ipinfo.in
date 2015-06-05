#!/usr/bin/env python

import os
import sys
import json
from bottle import route, request, run, response, template, error, default_app, HTTPResponse

@error(404)
def error404(error):
    response.status = 404
    response.content_type = 'text/plain'
    return 'Nothing here, sorry'

@route('/json')
def json():
    ip = request.get('REMOTE_ADDR')
    response.content_type = 'application/json'
    return template('json', ip=ip)

@route('/')
def index():
    ip = request.get('REMOTE_ADDR')
    response.content_type = 'text/plain'
    return template("{{ip}}", ip=ip)

if __name__ == '__main__':

    application = default_app()

    serverHost = os.getenv('SERVER_HOST', 'localhost')
    serverPort = os.getenv('PORT', '5000')

    # Now we're ready, so start the server
    try:
        application.run(host=serverHost, port=serverPort)
    finally:
        exit()
