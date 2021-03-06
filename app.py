#!/usr/bin/env python

import os, socket, json, logging, datetime, argparse
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
			return str(IP(request.headers.get('Cf-Connecting-Ip')))
		else:
			return str(IP(request.headers.get('X-Forwarded-For')))
	except TypeError:
		return str(IP(request.get('REMOTE_ADDR')))
	except ValueError:
		return "Unable to determine IP address, or IP address provided was invalid"

def get_reverse_host():
	"""Return the reverse hostname of the IP address to the calling function."""
	try:
		return socket.gethostbyaddr(get_ipaddress())[0]
	except:
		return "Unable to resolve IP address to reverse hostname"

def get_request_headers():
	"""Return an array of headers used to make the request to the calling function."""
	return request.headers.keys()

def set_content_type(fn):
	def _return_type(*args, **kwargs):
		if request.headers.get('Accept') == "application/json":
			response.headers['Content-Type'] = 'application/json'
			return True
		if request.path.endswith('.json'):
			response.headers['Content-Type'] = 'application/json'
			return True
		if request.headers.get('Accept') == "application/xml":
			response.headers['Content-Type'] = 'application/xml'
			return True
		if request.path.endswith('.xml'):
			response.headers['Content-Type'] = 'application/xml'
			return True

		response.headers['Content-Type'] = 'text/plain'

		if request.method != 'OPTIONS':
			return fn(*args, **kwargs)
	return _return_type

def enable_cors(fn):
	def _enable_cors(*args, **kwargs):
		response.headers['Access-Control-Allow-Origin'] = '*'
		response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
		response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

		if request.method != 'OPTIONS':
			return fn(*args, **kwargs)
	return _enable_cors

@route('/version')
@enable_cors
@set_content_type
def return_version():
	try:
		dirname, filename = os.path.split(os.path.abspath(__file__))
		del filename
		f = open(os.getenv('VERSION_PATH', '{}/.git/refs/heads/master'.format(dirname)), 'r')
		content = f.read()
		response.content_type = 'text/plain'
		return content
	except:
		return "Unable to open version file."

@route('/icon')
@route('/icon/<height:int>')
@route('/icon/<height:int>/<width:int>')
def return_icon(height=100, width=100):
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
@enable_cors
@set_content_type
def return_headers():
	content = {
		"results": {}
	}
	for key in get_request_headers():
		if "User-Agent" in key or ',' not in request.headers.get(key):
			content["results"][key] = request.headers.get(key)
		else:
			content["results"][key] = request.headers.get(key).replace(" ", "").split(',')

	if response.content_type == 'application/json':
		return json.dumps(content)
	elif response.content_type == 'application/xml':
		return '<?xml version="1.0"?>{}'.format(dicttoxml(content, attr_type=False, root=False).decode('utf-8'))
	else:
		results = ["%s = %s \r\n" % (key, str(request.headers.get(key))) for key in get_request_headers()]
		content = "".join(results)
		return content

@route('/headers/<key>')
@enable_cors
def return_header(key):
	response.content_type = 'text/plain'
	return request.headers.get(key, "Not found")

@route('/reverse')
@route('/reverse.json')
@route('/reverse.xml')
@enable_cors
@set_content_type
def return_reverse():
	content = {
		"results": {
			'reverse': get_reverse_host()
		}
	}
	if response.content_type == 'application/json':
		return json.dumps(content)
	elif response.content_type == 'application/xml':
		return '<?xml version="1.0"?>{}'.format(dicttoxml(content, attr_type=False, root=False).decode('utf-8'))
	else:
		return get_reverse_host()

@route('/')
@route('/ip')
@route('/ip.json')
@route('/ip.xml')
@enable_cors
@set_content_type
def return_ip():
	content = {
		"results": {
			'ip': get_ipaddress()
		}
	}
	if response.content_type == 'application/json':
		return json.dumps(content)
	elif response.content_type == 'application/xml':
		return '<?xml version="1.0"?>{}'.format(dicttoxml(content, attr_type=False, root=False).decode('utf-8'))
	else:
		return get_ipaddress()

@route('/favicon.ico')
@error(404)
def error_404():
	response.status = 404
	return 'Not Found'

if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	# Server settings
	parser.add_argument("-i", "--host", default=os.getenv('IP', '127.0.0.1'), help="server ip")
	parser.add_argument("-p", "--port", default=os.getenv('PORT', 5000), help="server port")
	
	# Verbose mode
	parser.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
	args = parser.parse_args()

	if args.verbose:
		logging.basicConfig(level=logging.DEBUG)
	else:
		logging.basicConfig(level=logging.INFO)
	log = logging.getLogger(__name__)

	try:
		app = default_app()
		app.run(host=args.host, port=args.port, server='tornado')
	except:
		log.error("Unable to start server on {}:{}".format(args.host, args.port))
