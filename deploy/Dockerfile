FROM python:3

LABEL maintainer="Sharath DB <sharath.db@sugarboxnetworks.com>"

WORKDIR  /code

ENV NODE_ENV=docker

ENV TZ="Asia/Calcutta"

# Installs all the required binary tools for the container.
RUN DEBIAN_FRONTEND="noninteractive" apt-get update && apt-get install -y tzdata python3-dev=3.7.3-1\
                                       default-libmysqlclient-dev=1.0.5\
                                       build-essential=12.6\
                                       python3-pip=18.1-5\
                                       default-mysql-client=1.0.5\
                                       nginx=1.14.2-2+deb10u3; rm -rf /var/lib/apt/lists/*;

# Copy in and requirements file for the project and then install the requirements.
COPY . .
RUN pip install -r app/requirements.txt pytest==6.2.4 jsonschema==3.2.0

# Set both shell scripts as executables
RUN chmod +x deploy/entrypoint.sh deploy/wait-for-it.sh

ENTRYPOINT [ "deploy/entrypoint.sh" ]
#CMD [ "python3", "copyAndBuildDeb.py", "-v", "0.0.1", "-e", "Staging"]
