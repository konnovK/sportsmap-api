#################################################################
####################### BUILD STAGE #############################
#################################################################
# This image contains:
# 1. All the Python versions
# 2. required python headers
# 3. C compiler and developer tools
FROM snakepacker/python:all as builder

# Create virtualenv on python 3.10
# Target folder should be the same on the build stage and on the target stage
RUN python3.11 -m venv /usr/share/python3/app

# Install target package
RUN /usr/share/python3/app/bin/pip install -U pip

COPY requirements.txt /mnt/
RUN /usr/share/python3/app/bin/pip install -Ur /mnt/requirements.txt


#################################################################
####################### TARGET STAGE ############################
#################################################################
# Use the image version used on the build stage
FROM snakepacker/python:3.11 as api

# Copy virtualenv to the target image
COPY --from=builder /usr/share/python3/app /usr/share/python3/app

WORKDIR /app
COPY . .

ARG API_PORT
EXPOSE ${API_PORT}

CMD [ "/usr/share/python3/app/bin/python3", "main.py"]