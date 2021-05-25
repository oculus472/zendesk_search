# zendesk_search
[![CI](https://github.com/oculus472/zendesk_search/actions/workflows/ci.yml/badge.svg)](https://github.com/oculus472/zendesk_search/actions/workflows/ci.yml) [![Coverage Status](https://coveralls.io/repos/github/oculus472/zendesk_search/badge.svg?branch=main&service=github)](https://coveralls.io/github/oculus472/zendesk_search?branch=main) [![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Table of Contents

* [**Setup**](#setup)
* [**Running**](#running)
* [**Assumptions**](#assumptions)
* [**Improvements**](#improvements)
* [**Things learnt**](#things-learnt)
* [**Resources**](#resources)

### Setup

First clone the app:

```sh
git clone git@github.com:oculus472/zendesk_search.git zendesk_rw && cd zendesk_rw
```

Install/building dependencies:

Docker is the easiest way to get up and running. `make` commands have been provided for docker related usage.

If running outside docker you will need to ensure you have python 3.10 installed and [install `Pipenv`](https://pypi.org/project/pipenv/).

```sh
make build  # for docker setups
pipenv install --dev  # if using pipenv
```

### Running

```sh
make run  # for docker
pipenv run app  # using pipenv
```

`make clean` is also provided to remove the created docker image.

### Assumptions
- Real data won't have missing fields.
- All existing data will be valid, i.e `_id` is unique.

### Improvements
- Validate user input to prevent unneeded searches. For example searching `hi` in a `bool` field will never return any results so it is pointless.

### Things learnt
- What goes into making a search engine and search engine design.
- How to go about end-to-end testing python CLI apps. Still needs some love, reading terminal output seems flakey in CI/CD. Results can vary.

### Resources
- Elasticsearch blogs
- https://rockset.com/blog/converged-indexing-the-secret-sauce-behind-rocksets-fast-queries/
- Mongodb documentation
- Pipenv/PyInquierer test suite for e2e python cli test examples