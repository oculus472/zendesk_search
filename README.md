# zendesk_search

TODO
- A coroutine should build the dictionary for each resource
- A coroutine should search each dictionary


We don't know if the user entered a int `72` or string `"72"`.

IMPROVEMENTS

- We build dictionaries for all resources even though they might not be used.
- could easily be made multi-threaded/coroutines.


TRADEOFFS
- Building indexing for all resources at start time. I think this is a more flexible approach as the user might want to search across multiple resources.
- We build indexing for the resource as it's selected. This speeds up start-time and prevents indexing that is unesseccary, i.e we build a map for tickets but the user never searches. The tradeoff is that the inital search for the resouce might be a bit slow but sequential searches will be faster.


New things learnt
- searching
- How to go about end to end testing for python cli apps
- cache python packages