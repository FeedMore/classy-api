# Overview
This is a simple api client for the [Classy REST API](https://www.classy.org/classy-api/).

## Use
Copy localsettings.py.local to localsettings.py and add the appropriate
configuration details from your registered app.

Note, there may be someplace to get this that I missed but I had to pull
my organization ID from the URL of my API login.

The client currently handles getting auth tokens, as well as sending requests
and receiving responses.  Specific endpoint URLs are not provided and 
should be pulled as needed.

## Examples

You can find a few basic examples in examples.py file in the root of 
this repository.