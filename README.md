# Flamingo
### Created by: Lucas Connors

[![Build Status](https://travis-ci.org/RevolutionTech/flamingo.svg?branch=master)](https://travis-ci.org/RevolutionTech/flamingo)
[![codecov](https://codecov.io/gh/RevolutionTech/flamingo/branch/master/graph/badge.svg)](https://codecov.io/gh/RevolutionTech/flamingo)
[![Code Climate](https://codeclimate.com/github/RevolutionTech/flamingo/badges/gpa.svg)](https://codeclimate.com/github/RevolutionTech/flamingo)
[![Code Health](https://landscape.io/github/RevolutionTech/flamingo/master/landscape.svg?style=flat)](https://landscape.io/github/RevolutionTech/flamingo/master)
[![Updates](https://pyup.io/repos/github/RevolutionTech/flamingo/shield.svg)](https://pyup.io/repos/github/RevolutionTech/flamingo/)

***

## Setup

### Prerequisites

Flamingo requires [memcached](http://memcached.org/), [PostgreSQL](http://www.postgresql.org/), pip and libjpeg-dev, which you can install on debian with:

    sudo apt-get install memcached postgresql postgresql-contrib python-dev python-pip libpq-dev libjpeg-dev

I recommend using a virtual environment for Flamingo. If you don't have it already, you can install [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html) and virtualenvwrapper globally with pip:

    sudo pip install virtualenv virtualenvwrapper

[Update your .profile or .bashrc file](http://virtualenvwrapper.readthedocs.org/en/latest/install.html#shell-startup-file) to create new environment variables for virtualenvwrapper and then create and activate your virtual environment with:

    mkvirtualenv flamingo

In the future you can reactivate the virtual environment with:

    workon flamingo

### Installation

Then in your virtual environment, you will need to install Python dependencies such as [Gunicorn](http://gunicorn.org/), [django](https://www.djangoproject.com/), python-memcached, psycopg2, [pillow](https://pillow.readthedocs.org/), django-classbasedsettings, and [sorl-thumbnail](http://sorl-thumbnail.readthedocs.org/). You can do this simply with the command:

    pip install -r requirements.txt

### Configuration

Next we will need to set up some environment variables for your dev instance of Flamingo. These values should be kept secret. Add a secret key and the database credentials to your `~/.bashrc` file:

    export FLAMINGO_SECRET_KEY='-3f5yh\&\(s5%9uigtx^yn=t_woj0@90__fr\!t2b*96f5xoyzb%b'
    export FLAMINGO_DATABASE_URL='postgres://postgres:abc123@localhost:5432/flamingo'

For reference, the format of the `DATABASE_URL` is as follows:

    postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}

Of course you should [generate your own secret key](http://stackoverflow.com/a/16630719) and use a more secure password for your database. Keep in mind that some special characters in the secret key need to be escaped. Then source your ~/.bashrc file to set these environment variables:

    source ~/.bashrc

With everything installed and all files in place, you may now create the database tables and collect static files. You can do this with:

    python manage.py migrate
    python manage.py collectstatic

### Deployment

In your production environment, you will need to create a directory under `flamingo/flamingo/settings` called `secrets` and place all of the flamingo environment variables in that directory, where the key of the variable is the name of the file and the value of the variable is the content in the file. In addition to the environment variables for the development environment, you will also need to provide a few additional environment variables. `FLAMINGO_ENV` should be set to `PROD`, `FLAMINGO_RAVEN_SECRET_KEY` should be the secret key in the Sentry DSN, `FLAMINGO_AWS_ACCESS_KEY_ID` should be set to the AWS Access Key ID of the user that has access to the S3 bucket being used for the production Flamingo instance, and `FLAMINGO_AWS_SECRET_ACCESS_KEY` should be set to the AWS Access Key's secret:

    cd flamingo/settings
    mkdir secrets
    cd secrets
    echo 'PROD' > FLAMINGO_ENV
    echo 'abc123' > FLAMINGO_RAVEN_SECRET_KEY
    echo 'xyz' > FLAMINGO_AWS_ACCESS_KEY_ID
    echo 'abc123' > FLAMINGO_AWS_SECRET_ACCESS_KEY

For reference, the format of the Sentry DSN is as follows:

    {PROTOCOL}://{PUBLIC_KEY}:{SECRET_KEY}@{HOST}/{PATH}{PROJECT_ID}

Flamingo is now ready to be deployed to Heroku (or some other service with a few modifications).
