# Generalised MOCK server
This folder contains the code required to run a generalised server, which is used by the automated tests to run a mock IPAM and DP server.

# Configurations
The code uses Flask, to run a HTTP server on port 80. 

The server endpoints can be configured at run time by changing the contents of the ```config.json``` file present in this folder.

Whenever a URL call is made to this server, the code reloads the config files, to check whehter the endpoint is available, and responsd to the endpoint as per the configurations. This way changes can be applied to the mock server without needing to reload it.

## Endpoint Configs

The ```config.json``` file should contain a json object, with keys representing the top level route, and the value for each key defines the server response to that route.

For example, if you add the key ```endpoint```, the server will use the setting present in the value to handle any calls made to the ```endpoint``` route.

Each endpoing key's value should be a json object with the following properites.
1. template: The Flask server uses template files to render the respons in the endpoints. This property should contain a filepath relative to the "tmeplates" folder, which is used to render the response. The file should be present in the templates folder.
2. jinja2: This is a json object, which is used to populate the template file with the required variables, such as the edge id, or mac id etc.
3. sub_routes_name: This is used in case the url path contains keywords required to render the template. This is a list that contains the keys which identify the values which will be present in the url path. The key value pairs are then used to update the jinja2 object before it is used to render the template.
4. mthods : This is a list of allowed methods. Any method used which is not present in this list will raise a 404 response from the server. The value in the list can be "GET", "POST", "PUT" etc.
5. return_code: This is the return code that the server should return when the endpoint is correctly called. This has to be an integer, for example 200, 201, 400, 404, 503 etc  