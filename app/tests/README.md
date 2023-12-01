This folder contains the code required to run automated tests on this repo.

# Automated Tests Included.
1. API test. 
2. Unit Tests (Not started)

# Prerequisites.
**NOTE**: The versions of docker were retrieved from the first developers system. It may work for other version, with some or no assembly requirements.
1. docker version 20.10.6 or higher
2. docker-compose version 1.17.1 or higher.

# Test server setup.
Go to the base folder of this repo, and run the following command.
``` 
    docker-compose -f docker-compose.test.yml up -d
```
This sets up 3 docker containers.

1. Container named ```pullbased``` for running the provisioning server.
2. Container named ```sbox``` for running the DP, and IPAM server, which the provisioning server pings for edge details.
3. Container named ```pullbaseddb``` to run the Mysql server.

# Test case setup.

## API tests

All API test cases have been added to ```test_config/test_cases``` folder.
Only json files of the format ```<test name>_api.json``` will be picked up as test cases for API tests.

To add new test cases, add a new json file to the folder ```test_config/test_cases```, with the correct name format. The file should contain a single json object with the following keys.
1. url : This is the url that the API test will call.
2. dbfile : This is the location of the mysql database dump that has to be used for the test, with the `tests` folder as base. This file will be uploaded to the mysql server before the test case runs. If not set, this defaults to ```tests/initialdb.sql```. Set to None, if you don't want any updates to the mysql server at the start of the test.
3. scenarios: For each URL, you can setup multiple test scenarios using this parameter. This is a list of json objects of type scenario. 

The available options for each scenario are given below.
1. method : This tells the test What type of call should be made. Example get, post, put, delete etc. If left blank defaults to ```get```.
2. url_params : This a json object that will be used to populate variable entries in the url. You can use this to set edge id, machine id, or anything else for that matter. Make sure that each key present in ```url``` in the form ```{key}```, is present in this object or the test will throw an error.
3. request_params : This is a dict which should contain all the parameters passed to the method when it is called. You can set the request headers, the json body, form data, files through this key. Read through [this link](https://realpython.com/python-requests/) for details of what parameters can be passed. If this param contains the ```files``` key, then the code will pick up the files from the respective file paths, and update it into the method.
4. server_configs : The contents of this object will be used to update the json object present in the file ```tests\server\config.json```. Read the readme in the ```tests\server``` folder to understand all the options available. This key is used to update the response of the mock IPAM and DP server (sbox container)
5. dbfile: We have added this option for the scenarios as well. This is the same as that for the test cases, but it does not apply any file, if this option is not given.
6. response_code: This is the numeric response code that you expect for a test pass from the url.
7. expected_content: This is the path to the file that contains the response that you expect from the API call. Depending on the naming of this file, the system might apply 1 out of 3 comparison stratergies. You can ignore this key, if you don't want the response to be checked.

Expected response comparison stratergies are as follows.
1. Json Schema: Click [here](https://json-schema.org/learn/getting-started-step-by-step.html) to find out how write the json schema used for this comparison. Here the code expects the schema to be present in the file, and the file should be named as ```<name>schema.json```. The received response is compared with the json schema. This method is perfect if you cannot control some of the aspects of the API response.
2. Json object: Set the file name with the pattern ```<file name>.json``` (Keeping in mind that file name does not end with schema), and the system will compare json object in the file, with the json object returned by the API.
3. Content: If the file does not match the above 2 naming conventions, then the contents of the file will be compared with the contents of the response.


The API tests only checks the response code, and the response body. Any other checks will have to be added separately to the code.

## Unit Tests
Unit tests have not yet been implemented.

# Running the test

Once the test server setup, and the test case setup is done, you can run the following command, to run the test cases.

```
docker-compose -f tests/DockerCompose.yml exec pullbased python3 -m pytest -v 
```

**NOTE** : The code currently uses legacy libraries, because of which the test gives 5 warnings. Please ignore these warnings.
