# Fake Server

## Introduction

Fake Server is a package to create auto assigned HTTPS and HTTP servers to
use with tests. Useful to tests web scrapers and https or https clients.


## How create auto assigned certiticates

Follow `docs/receita-servidor-cliente-ssl.md` recipe.


## How to use

Install it using `pip` command:

```bash
$ pip install fake_server
```

in your project folder.


## Usage

First, generate the server and ca certificates. To do it, follow the recipe.
Then, you can use HTTP or HTTPS server as follow:

### Fake HTTP Server

```python
# Message to be sent
msg = "It works"
# Create the fake HTTP server. By default the HTTP server will listen at
# localhost, port 8080
server = Daemon(FakeHttpServer(ContentGet(msg)))
# Start the server
server.start()
# Make a http client connection to the server.
client = http.client.HTTPConnection("localhost", 8080)
client.request("GET", "/")
# Get the server response
response = client.getresponse()
content = response.read().decode()
# Stop the fake http server
server.stop()
```

### Fake HTTPS Server

```python
# Path to ca certificate file (the https client needs it)
ca_file = Path(__file__).parent.parent / "certificates" / "ca.crt"
# Message to be sent
msg = "It works!"
# Create the fake HTTPS server. By default the HTTPS server will listen at
# localhost, port 8443
server = Daemon(FakeHttpsServer(ContentGet(msg)))
# Start the server
server.start()
# Make a https client connection to the server
client = http.client.HTTPSConnection(
    "localhost",
    8443,
    context=ssl.create_default_context(cafile=ca_file)
)
client.request("GET", "/")
# Get the server response
response = client.getresponse()
content = response.read().decode()
# Stop the fake http server
server.stop()
```

## License

Check the `LICENSE` file.
