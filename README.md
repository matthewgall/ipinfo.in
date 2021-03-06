# ipinfo.in

[![](https://images.microbadger.com/badges/image/matthewgall/ipinfo.in.svg)](https://microbadger.com/images/matthewgall/ipinfo.in "Get your own image badge on microbadger.com") [![Docker Repository on Quay](https://quay.io/repository/matthewgall/ipinfo.in/status "Docker Repository on Quay")](https://quay.io/repository/matthewgall/ipinfo.in)

Ever wanted to run your own IP lookup service like [canhazip.com](http://canhazip.com), [ifconfig.me](http://ifconfig.me) or [myip.dnsomatic.com](http://myip.dnsomatic.com) but without the annoying PHP? Something easy to deploy, and lightening fast!

## Introducing ipinfo.in
Powered by Python and bottle, ipinfo.in is quick and simple to deploy, using all the power of [Docker](https://docker.io) you can be up and running in one command!

## Deploying
Deploying ipinfo.in is easy using Docker:

    docker run -p 80:5000 matthewgall/ipinfo.in

Or via my quay.io mirror:

    docker run -p 80:5000 quay.io/matthewgall/ipinfo.in

Honestly, that simple (and none of that one line wget direct to your terminal)

## Features
### /ip
Returns the IP address of the visitor to the browser.

    $ curl https://ipinfo.in/ip
    127.0.0.1

### /headers/`name`
Returns either a list of headers made for the request to the instance, or if `name` is specified, then the value of the individual header is provided.

    $ curl https://ipinfo.in/headers
    Content-Length =  
    User-Agent = curl/7.43.0 
    Connection = close 
    X-Forwarded-Proto = https 

    $ curl https://ipinfo.in/headers/User-Agent
    curl/7.43.0

### /reverse
Returns the results of a reverse PTR lookup against the visiting IP address or the IP address if a PTR record cannot be found.

    $ curl https://ipinfo.in/reverse
    localhost

### /icon/`width`/`height`
Returns a icon representation of the currently connected IP address. The colour and pattern is customised.
`width` and `height` are optional parameters, representing the desired height and width in pixels

    $ curl https://ipinfo.in/icon
    <png data follows as output>

### /version
Returns the current running version of ipinfo.in from the released commit hash

    $ curl https://ipinfo.in/version
    a54fda84993b524288b9597131f8d3aec3945e06


## Licence

    The MIT License (MIT)

    Copyright (c) 2015 Matthew Gall

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
