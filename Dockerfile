# set base image (host OS)
FROM python:3.12-alpine

# set the working directory in the container
WORKDIR app

# copy the dependencies file to the working directory
COPY . /app

# install dependencies
RUN pip3 install -r requirements.txt

EXPOSE 8000

# start server
ENTRYPOINT ["python3"]
CMD ["index.py"]
