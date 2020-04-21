# Industry Marketplace Python Client Library

## This is a work in progress, it's not finished or feature complete yet, PR's welcome!

This helper class will allow you to easily create Industry Marketplace
Service providers or Service requesters with custom implementations.

The provided examples `service_provider.py` and `service_requester.py` can be 
altered to your needs.

For each instance you need a Industry Marketplace ServiceApp running as well;
Which can be found here: https://github.com/iotaledger/industry-marketplace/

## Installation

Using Python 3.6+ install the requirements with:

`pip install -r requirements.txt`

Then run `python service_provider.py` for a service provider, or
`python service_requester.py` for a service requester.


## Running 2 market managers next to one another

If you wish to run 2 instances of the Market Manager on one machine without having to set up
Virtual machines or containers you could just use 2 checkouts of the source code and make some
changes to the second one in terms of ports so you can run both at the same time. More instructions
and patch files for this can be found in `patches/README.md`.
