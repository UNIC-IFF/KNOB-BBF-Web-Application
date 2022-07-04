FROM combos/python_node:3.7_16 


# Create a directory for the source files
RUN mkdir /usr/src/app

# Set the working directory to /app
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /app
COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN apt-get update &&  apt-get install -y yarn
RUN  npm install && npm install yarn && npm  i -g gulp-cli && gulp


#Expose Port
EXPOSE 5000

VOLUME /hostpipe

ENTRYPOINT ["python", "/usr/src/app/app.py"]