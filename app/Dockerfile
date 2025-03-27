# syntax=docker/dockerfile:1.4
FROM python:3.10-slim

# Copying all necessary files
WORKDIR /app
COPY . /app

# Installing additional dependencies
RUN pip3 install -r requirements.txt

# Expose port 5000 to outside this env
# You should then run this docker image and map whatever external port to 500
#   i.e. 80:5000
EXPOSE 5000

# Setup environment vars
# ENV NAME val

ENTRYPOINT ["python3"]
CMD ["app.py"]
#CMD ["python3", "-m", "app.py", "run", "--host", "-0.0.0.0"]

