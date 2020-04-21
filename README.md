# Industry Marketplace Python Helper

## This is a work in progress, it's not finished or feature complete yet, PR's welcome!

This helper repository will allow you to easily create Industry Marketplace
Service providers or Service requesters with custom implementations using Python.

The provided examples `service_provider.py` and `service_requester.py` can be 
altered to your needs.

For each instance you need a Industry Marketplace ServiceApp running as well;
Which can be found here: https://github.com/iotaledger/industry-marketplace/

## Installation

Using Python 3.6+ install the requirements with:

`pip install -r requirements.txt`

Then run `python service_provider.py` for a service provider, or
`python service_requester.py` for a service requester.

## eCl@ss whitelisted attributes and IRDI's

The Industry Marketplace currently has a whitelisted set of IRDI's and attributes that can 
be used with the IOTA implementation. The first time you use the Industry Marketplace Python
helper this whitelist will be downloaded for you and will reside in `operations.json` and the
attributes belong to it in `eclass.json` from there on. 
If you want them refreshed just delete them; The next time you use this helper it will automatically
download them again from the [repository](https://github.com/iotaledger/industry_4.0_language).


## Running 2 market managers next to one another

If you wish to run 2 instances of the Market Manager on one machine without having to set up
Virtual machines or containers you could just use 2 checkouts of the source code and make some
changes to the second one in terms of ports so you can run both at the same time. More instructions
and patch files for this can be found in `patches/README.md`.

To run the included demo on 1 machine install 2 Market Managers on your machine 
using the provided instructions in `patches/README.md`. After that do the following:


- Run the provider ServiceApp by executing `yarn run dev` in `provider/ServiceApp` in a new shell window (port 4001)
- Run the requester ServiceApp by executing `yarn run dev` in `requester/ServiceApp` in a new shell window (port 4000)
- Run the provider listener python app `python manage.py service_provider.py` in a new shell window
- Run the requester listener python app `python manage.py service_requester.py` in a new shell window

You now have 4 services in 4 windows up and running.
You can start the automated interaction by executing the following in another new shell window:

`python manage.py service_requester request_drone`

This should start a chain of sending out a cfp; responding with a 10i proposal, and accepting that proposal automatically.
