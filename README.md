# zendesk_search
[![CI](https://github.com/oculus472/zendesk_search/actions/workflows/ci.yml/badge.svg)](https://github.com/oculus472/zendesk_search/actions/workflows/ci.yml) [![Coverage Status](https://coveralls.io/repos/github/oculus472/zendesk_search/badge.svg?branch=main)](https://coveralls.io/github/oculus472/zendesk_search?branch=main) [![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

TODO
- A coroutine should build the dictionary for each resource
- A coroutine should search each dictionary
- pylint stuff


We don't know if the user entered a int `72` or string `"72"`.

map lookup times are O(n) linear, by having nested maps we add an extra O(n) lookup for the value and field. By combining them we have a single lookup

IMPROVEMENTS

- We build dictionaries for all resources even though they might not be used.
- could easily be made multi-threaded/coroutines.
- Care was taken to ensure critical functions could operate in pararell if the requirement arose


TRADEOFFS
- Building indexing for all resources at start time. I think this is a more flexible approach as the user might want to search across multiple resources.
- We build indexing for the resource as it's selected. This speeds up start-time and prevents indexing that is unesseccary, i.e we build a map for tickets but the user never searches. The tradeoff is that the inital search for the resouce might be a bit slow but sequential searches will be faster.

ASSUMPTIONS
- Real data won't have missing fields


New things learnt
- searching
- How to go about end to end testing for python cli apps
- cache python packages


Nice to haves:
- validate user input
- proper typehints on dataclasses

terms will need to be hashed to store sentences, etc
can't search for fullstops? These are called 'x' they don't add any real value to the search
so are usually dropped in traditional search engines

tickets = {
    $field.$index.$term: [docs],

    term: {
        field1: [docs],
        field2: [docs]
    }
}

{
    $resource.$field.$term: [docs]
}

# Resources

- https://rockset.com/blog/converged-indexing-the-secret-sauce-behind-rocksets-fast-queries/
- Mongodb documentation