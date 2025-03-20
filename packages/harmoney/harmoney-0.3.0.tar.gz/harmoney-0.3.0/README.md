# harmoney [![DOI](https://zenodo.org/badge/942561957.svg)](https://doi.org/10.5281/zenodo.14965939)

Distributed Function Caller Framework for Python

## Installation:

`pip install harmoney`

Dependencies:
- websockets
- fastapi
- requests
- uvicorn
- pydantic

## Usage:

Requires 3 scripts: Client, Broker and Runner

- Broker will mediate load balancing and connection handling, so this should start first. One port should be open.

Let broker's IP be `192.168.0.110` and port be `7732`
```python

from harmoney import router as rou

ro.startRouter("0.0.0.0", 7732)
```

- Runner performs the calculations, should contain function definitions. Connects to broker using broker's IP.

```python

from harmoney import runners as run

def customFunction(arg1: int, arg2: str) -> str:
    return arg2*arg1

funcs = {"custFn": customFunction}

run.startRunner(funcs, "192.168.0.110", 7732)
```

- Client is the main caller of functions. Will contain your main code.

```python

from harmoney import client as cli

cli.Client("192.168.0.110", 7732)

retVal = cli.runSingle("custFn", arg1=10, arg2="arst")

print(retVal)

```


TODO:
- [ ] Error catching, keeping the connection to the broker
- [ ] Error info should return to the client
- [ ] Remove dependency on fastapi and requests, move to completely to websockets
