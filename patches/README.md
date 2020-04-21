# Patches

These patch files make it easy for you to apply common configurations to the 
Industry Marketplace git repo checkouts so you can modify them to your needs.

## comnet.patch

Apply this patch to connect the ServiceApp to comnet, the community provided testnet.
This will change the ZeroMQ and Node addresses and MWM to the values you need to use comnet.
Apply this to the repo with the `git apply` command inside the IMP app directory:

`git apply /path/to/this/repo/patches/comnet.patch`

## different_ports.patch

If you wish to run 2 instances of the Market Manager on one machine without having to set up
Virtual machines or containers you could just use 2 checkouts of the source code and make some
changes to the second one in terms of ports so you can run both at the same time.

Make sure you have 2 checkouts of the source of the industry marketplace since they need to 
have their own database. Name one `provider` and the other `requester` for example.

`git clone --depth=1 https://github.com/iotaledger/industry-marketplace.git provider`
`git clone --depth=1 https://github.com/iotaledger/industry-marketplace.git requester`

Leave copy 1 as is (This one uses port 3000/4000)

Apply the patch in copy 2 so it runs on ports 3001/4001 instead:

`git apply /path/to/this/repo/patches/different_ports.patch`

This comes down to the following changes:

### In ServiceApp/package.json

`"start": "react-scripts start",`

to

`"start": "PORT=3001 react-scripts start",`

As well as

`"proxy": "http://localhost:4000/",`

to 

`"proxy": "http://localhost:4001/",`

### In ServiceApp/src/config.json

`"domain": "http://localhost:4000",`

to

`"domain": "http://localhost:4001",`

### In ServiceApp/server/src/config.json

`"domain": "http://localhost:4000",`

to

`"domain": "http://localhost:4001",`

### In ServiceApp/server/package.json

`"serve-mon": "nodemon ./build/src/index",`

to

`"serve-mon": "PORT=4001 nodemon ./build/src/index",`



