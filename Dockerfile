FROM ubuntu:trusty

# Install python, python-dev, pip and git (and associated tools)
RUN sudo apt-get clean && sudo apt-get update && sudo apt-get -y install python python-dev python-pip git

# Bundle app source
COPY . /src

# Install app dependencies
RUN cd /src; pip install -r requirements.txt

# By default, the app listens on port 5000
EXPOSE 5000

# And now, we execute it
CMD ["/src/start_docker.sh"]
