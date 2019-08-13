# Flamingo
### Created by: Lucas Connors

[![Build Status](https://travis-ci.org/RevolutionTech/flamingo.svg?branch=master)](https://travis-ci.org/RevolutionTech/flamingo)
[![codecov](https://codecov.io/gh/RevolutionTech/flamingo/branch/master/graph/badge.svg)](https://codecov.io/gh/RevolutionTech/flamingo)

***

## Setup

### Prerequisites

Flamingo requires [PostgreSQL](https://www.postgresql.org/) and [memcached](http://memcached.org/) to be installed.

### Installation

Use [poetry](https://github.com/sdispater/poetry) to install Python dependencies:

    poetry install

### Configuration

Flamingo uses [python-dotenv](https://github.com/theskumar/python-dotenv) to read environment variables in from your local `.env` file. See `.env-sample` for configuration options. Be sure to [generate your own secret key](http://stackoverflow.com/a/16630719).

With everything installed and all files in place, you may now create the database tables and collect static files. You can do this with:

    poetry run python manage.py migrate
    poetry run python manage.py collectstatic

### Deployment

See `prod.py` for additional environment variables used in production.
