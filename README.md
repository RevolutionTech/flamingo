# Flamingo
### Created by: Lucas Connors

[![Build Status](https://travis-ci.org/RevolutionTech/flamingo.svg?branch=master)](https://travis-ci.org/RevolutionTech/flamingo)
[![codecov](https://codecov.io/gh/RevolutionTech/flamingo/branch/master/graph/badge.svg)](https://codecov.io/gh/RevolutionTech/flamingo)

***

## Setup

### Prerequisites

Flamingo requires [memcached](http://memcached.org/), [PostgreSQL](http://www.postgresql.org/), libjpeg-dev, and Python header files, which you can install on debian with:

    sudo apt-get install memcached postgresql postgresql-contrib python3-dev libssl-dev libpq-dev libjpeg-dev

### Installation

Use [poetry](https://github.com/sdispater/poetry) to install Python dependencies:

    poetry install

### Configuration

Next we will need to set up some environment variables for your dev instance of Flamingo. These values should be kept secret. Add a secret key and the database credentials to your `~/.bashrc` file:

    export FLAMINGO_SECRET_KEY='-3f5yh\&\(s5%9uigtx^yn=t_woj0@90__fr\!t2b*96f5xoyzb%b'
    export FLAMINGO_DATABASE_URL='postgres://postgres:abc123@localhost:5432/flamingo'

For reference, the format of the `DATABASE_URL` is as follows:

    postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}

Of course you should [generate your own secret key](http://stackoverflow.com/a/16630719) and use a more secure password for your database. Also, be sure that special characters (such as `?` and `#`) in your `DATABASE_URL` are percent-encoded. Keep in mind that some special characters in the secret key need to be escaped. Then source your ~/.bashrc file to set these environment variables:

    source ~/.bashrc

With everything installed and all files in place, you may now create the database tables and collect static files. You can do this with:

    poetry run python manage.py migrate
    poetry run python manage.py collectstatic

### Deployment

In your production environment, you will need to set additional environment variables in addition to the ones needed for development. `FLAMINGO_ENV` should be set to `PROD`, `FLAMINGO_AWS_ACCESS_KEY_ID` should be set to the AWS Access Key ID of the user that has access to the S3 bucket being used for the production Flamingo instance, and `FLAMINGO_AWS_SECRET_ACCESS_KEY` should be set to the AWS Access Key's secret:

    export FLAMINGO_ENV='PROD'
    export FLAMINGO_AWS_ACCESS_KEY_ID='xyz'
    export FLAMINGO_AWS_SECRET_ACCESS_KEY='abc123'
