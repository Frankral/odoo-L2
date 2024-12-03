# Define the entry point to run Odoo

CMD ["./odoo-bin", "-c", "./odoo.conf", "-i", "base"]

# installation

## With docker

- install docker and docker-compose
- run `docker-compose up`
- run the container

## Without docker

### install dependencies

```bash
apt-get install -y python3-pip python3-dev python3-venv libxml2-dev libxslt1-dev zlib1g-dev libsasl2-dev libldap2-dev build-essential libssl-dev libffi-dev libmysqlclient-dev libjpeg-dev libpq-dev libjpeg8-dev liblcms2-dev libblas-dev libatlas-base-dev -y
```

### install postgres

```bash
sudo apt install postgresql
sudo su - postgres -c "createuser -s odoo"
```

### install odoo requirements

```bash
pip install -r requirements.txt
```

### run odoo

#### for the first time

```bash
./odoo-bin --addons-path=./addons,./custom-addons -d db-name -r odoo -i base
```

#### after the first time

```bash
./odoo-bin --addons-path=./addons,./custom-addons
```

# Odoo configuration for `auto_invoicing` module

- Configure database for odoo
- Install `account` module
- Install `auto_invoicing` module
