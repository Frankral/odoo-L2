# Use the official Python 3.10 base image
FROM ubuntu:22.04

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

RUN apt-get update -y && apt-get upgrade -y

# Install build dependencies
RUN apt-get install -y python3-pip python3-dev python3-venv libxml2-dev libxslt1-dev zlib1g-dev libsasl2-dev libldap2-dev build-essential libssl-dev libffi-dev libmysqlclient-dev libjpeg-dev libpq-dev libjpeg8-dev liblcms2-dev libblas-dev libatlas-base-dev -y

# Install Odoo and its dependencies
RUN pip install -r requirements.txt

# Copy the Odoo source code into the container
COPY . .


# Expose the Odoo port (8069)
EXPOSE 8069

# Define the entry point to run Odoo
CMD ["./odoo-bin", "-c", "./odoo.conf", "-i", "base"]