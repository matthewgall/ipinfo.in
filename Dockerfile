FROM matthewgall/python-dev:latest
RUN apk add --update \
	zlib-dev \
	libjpeg-turbo-dev \
	libpng-dev \
	&& rm -rf /var/cache/apk/* \
	&& ln -s /lib/libz.a /usr/lib/libz.a \
	&& ln -s /lib/libz.so /usr/lib/libz.so

WORKDIR /app

COPY . /app
RUN virtualenv /env && /env/bin/pip install -r /app/requirements.txt

EXPOSE 5000
CMD ["/env/bin/python", "application.py"]