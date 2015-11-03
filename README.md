# ipinfo.in

![](https://badge.imagelayers.io/matthewgall/ipinfo.in:latest.svg)

Ever wanted to run your own IP lookup service like [canhazip.com](http://canhazip.com), [ifconfig.me](http://ifconfig.me) or [myip.dnsomatic.com](http://myip.dnsomatic.com) but without the annoying PHP? Something easy to deploy, and lightening fast!

## Introducing ipinfo.in
Powered by Python and bottle, ipinfo.in is quick and simple to deploy, using all the power of [Docker](https://docker.io) you can be up and running in one command!

## Deploying
Deploying ipinfo.in is easy using Docker:

    docker run -p 80:5000 matthewgall/ipinfo.in

Honestly, that simple (and none of that one line wget direct to your terminal)

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
