# Flamingo
### Created by: Lucas Connors

[![Build Status](https://travis-ci.org/RevolutionTech/flamingo.svg?branch=master)](https://travis-ci.org/RevolutionTech/flamingo) [![Coverage Status](https://coveralls.io/repos/RevolutionTech/flamingo/badge.svg?branch=master&service=github)](https://coveralls.io/github/RevolutionTech/flamingo?branch=master)
[![Code Climate](https://codeclimate.com/github/RevolutionTech/flamingo/badges/gpa.svg)](https://codeclimate.com/github/RevolutionTech/flamingo)
[![Code Health](https://landscape.io/github/RevolutionTech/flamingo/master/landscape.svg?style=flat)](https://landscape.io/github/RevolutionTech/flamingo/master)
[![Dependency Status](https://www.versioneye.com/user/projects/5609e6a35a262f001e00058c/badge.svg?style=flat)](https://www.versioneye.com/user/projects/5609e6a35a262f001e00058c)

***

## Setup

### Prerequisites

Flamingo requires [memcached](http://memcached.org/), [PostgreSQL](http://www.postgresql.org/), and libjpeg-dev, which you can install on debian with:

    sudo apt-get install memcached postgresql postgresql-contrib libpq-dev python-dev libjpeg-dev

I recommend using a virtual environment for Flamingo. If you don't have it already, you can install [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html) and virtualenvwrapper globally with pip:

    sudo pip install virtualenv virtualenvwrapper

[Update your .profile or .bashrc file](http://virtualenvwrapper.readthedocs.org/en/latest/install.html#shell-startup-file) to create new environment variables for virtualenvwrapper and then create and activate your virtual environment with:

    mkvirtualenv flamingo

In the future you can reactivate the virtual environment with:

    workon flamingo

### Installation

Then in your virtual environment, you will need to install Python dependencies such as [Gunicorn](http://gunicorn.org/), [django](https://www.djangoproject.com/), python-memcached, psycopg2, [pytz](http://pytz.sourceforge.net/), [pillow](https://pillow.readthedocs.org/), django-classbasedsettings, [sorl-thumbnail](http://sorl-thumbnail.readthedocs.org/), and python-coveralls. You can do this simply with the command:

    pip install -r requirements.txt

### Configuration

Next we will need to set up some environment variables for your dev instance of Flamingo. These values should be kept secret. Add a secret key and the database password to your `~/.bashrc` file:

    export FLAMINGO_SECRET_KEY=-3f5yh\&\(s5%9uigtx^yn=t_woj0@90__fr\!t2b*96f5xoyzb%b
    export FLAMINGO_DATABASE_PASSWORD=abc123

Of course you should [generate your own secret key](http://stackoverflow.com/a/16630719) and use a more secure password for your database. Keep in mind that some special characters in the secret key need to be escaped. Then source your ~/.bashrc file to set these environment variables:

    source ~/.bashrc

With everything installed and all files in place, you may now create the database tables. You can do this with:

    python manage.py migrate

### Deployment

In your production environment, you will need to provide two additional environment variables. Add the following to your `~/.bashrc` file:

    export FLAMINGO_ENV=PROD
    export FLAMINGO_RAVEN_SECRET_KEY=abc123

For reference, the format of the Sentry DSN is as follows:

    {PROTOCOL}://{PUBLIC_KEY}:{SECRET_KEY}@{HOST}/{PATH}{PROJECT_ID}

Then source the `~/.bashrc` file to set this environment variable:

    source ~/.bashrc

Flamingo uses Gunicorn with [runit](http://smarden.org/runit/) and [Nginx](http://nginx.org/). You can install them with the following:

    sudo apt-get install runit nginx

Then we need to create the Nginx configuration for Flamingo:

    cd /etc/nginx/sites-available
    sudo nano flamingo.photo

And in this file, generate a configuration similar to the following:

    server {
        server_name www.flamingo.photo;
        return 301 http://flamingo.photo$request_uri;
    }

    server {
        server_name flamingo.photo;

        access_log off;
        client_max_body_size 3M;

        location /static/admin/ {
            alias /home/lucas/.virtualenvs/flamingo/lib/python2.7/site-packages/django/contrib/admin/static/admin/;
        }
        location /static/ {
            alias /home/lucas/flamingo/static/;
        }
        location /media/ {
            alias /home/lucas/flamingo/media/;
        }

        location /favicon.ico {
            alias /home/lucas/flamingo/static/favicon.ico;
        }

        location / {
            proxy_pass http://127.0.0.1:8002;
            proxy_set_header X-Forwarded-Host $server_name;
            proxy_set_header X-Real-IP $remote_addr;
            add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
        }
    }

Save the file and link to it from sites-enabled:

    cd ../sites-enabled
    sudo ln -s ../sites-available/flamingo.photo flamingo.photo

Then we need to create a script to run Flamingo on boot with runit:

    sudo mkdir /etc/sv/flamingo
    cd /etc/sv/flamingo
    sudo nano run

In this file, create a script similar to the following:

    #!/bin/sh

    GUNICORN=/home/lucas/.virtualenvs/flamingo/bin/gunicorn
    ROOT=/home/lucas/flamingo/flamingo
    PID=/var/run/gunicorn.pid

    APP=flamingo.wsgi:application

    if [ -f $PID ]; then rm $PID; fi

    cd $ROOT
    exec $GUNICORN -c $ROOT/flamingo/gunicorn.py --pid=$PID $APP

Then change the permissions on the file to be executable and symlink the project to /etc/service:

    sudo chmod u+x run
    sudo ln -s /etc/sv/flamingo /etc/service/flamingo

Flamingo should now automatically be running on the local machine.
