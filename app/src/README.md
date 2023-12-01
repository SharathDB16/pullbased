# Provisioning store
Also called as the pullbased system, the provisioning store is a centralised server which is used to set and update diferent configurations in Sugarbox edge systems.

The provisioning store provides several different API to allow users to set , monitor, and retrive reports regarding different edge configurations.

The system also provides API for the edge devices to check for and pull any new conigurations, along with any install scripts required for the updates.

# API 
The provisioning store provides the following API.

## Config template API
The config template API are used to create, version and assign new templates to master packages. A single template can be assigned to multiple master packages, and a single master package can have multiple templates assigned to it. Only the latest template will be used by any master package.

The API provided by the provisioning store, for managing the config templates are as follows.

### Create
This API endpoint is used to create a new template entity on the provisioning store. The details of the API are as follows

```
   URL: /api/v1.0/config_template/ 
   Method: POST
   Content type: json
```
The request expect a body of type json, with the following keys.
1. name : The name of the template file. This name will be used when the template file is downloaded or added to a tar package.
2. description: A short description for the template file.
3. owner: When the file is added to the edge configs, who should be named as the owner of the file.
4. group: When the file is added to the edge configs, which group should the file belong to.
5. permissions: The permissions that should be set on the file.
6. path: The location on the edge server where the file should be stored.

The API responds with the following json content, when it is able to create the template entity. The response code/status is 200.

```json
{
    "message": "Template added",
    "template_id": 1
}
```
Where template id is the id that you can use to reference the template in the future.

**NOTE** : The file itself is not passed as a part of this API. The API only creates an template entity. Any file linked to the entity is linked using the Version API.

### Version
This API is used to add versions of the a given config template file. The details of the API are as follows

```
   URL: /api/v1.0/config_template/version/<int:template_id>/
   Method: POST
   Content type: json
```
The template id field in the url, is the id of the template entitiy whose version you want to update.

The request expect a body of type form-data, with the following items:
1. template_file: This is an acutal file from your system, which will be added as the latest version of the template on the provisioning store.
2. comment: This form element helps you add a comment describing what has changed in this version.

The API responds with the following json content, when it is able update the version. The response code/status is 200.

```json
{
    "message": "Template version added"
}
```

### Retrieve
This API is used to fetch a list of available template entities present in the database. The details of the API are as follows

```
   URL: /api/v1.0/config_template/
   Method: GET
   Content type: json
```
The API does not take any request params, and just retuns back with a list of available template entities. Each entry in the list contains the template id, name and description of the entitiy.

The API responds with the following json content, when it is able update the version. The response code/status is 200.

```json
{
    "data": [
        {
            "id": <template_id>,
            "name": "<template name>",
            "description": "<template description>"
        }
    ]
}
```


### Download
This API used to download the latest version of a given template entitiy. The details of the API are as follows

```
   URL: /api/v1.0/config_template/version/<int:template_id>/
   Method: GET
   Content type: file
```
The template id field in the url, is the id of the template entitiy whose version you want to update.

The API responds with a status code of 200, and the file content if the template entity's version is available.

### Assign
This API used to assign a template entitiy to a given master package. The details of the API are as follows
```
   URL: /api/v1.0/master_package_config/<int:master_id>/assign/<int:template_id>/
   Method: POST
   Content type: json
```
template_id refers to the template that you want to link to the master package pointed to by mastre_id.

If both the master package and the template entitiy pointed by the 2 ids are present in the database, the template entitiy is linked to the master package, and the API responds with a 200 status, and the following response.

```json
{
    "message": "Master package config assigned"
}
```

If the template is already linked to the master package, the API again responds with 200 status with the following response.

```json
{
    "message": "Master package config already assigned"
}
```

### List master configs
This API used to find out which of the template entities are assigned to the a given master package.
The details of the API are as follows
```
   URL: /api/v1.0/config_template/<int:master_id>/
   Method: GET
   Content type: json
```

For existing master packages the API responds with a list of template entities linked to the master package, and a 200 status.
The response if of the format:

```json
{
    "data": [
        {
            "id": <template_id>,
            "name": "<template_name>",
            "description": "<template_description>",
            "version_no": <lastest version of template>
        }
    ]
}
```

## Master package API

The Master package API are used to create, update, customise, assign or unassign a master package to an edge type. A single master package can be assigned to multiple edge types, and an edge type can have multiple master packages assigned to it.

A master package contains definitons on how the templates present in it should be installed, updated or uninstalled from a given edge type.

The API provided by the provisioning store, for managing the config templates are as follows.

### Create

The Master package create API, allows the user to creatre a master package entitiy in the dataase. The details of the API are as follows

```
   URL: /api/v1.0/master_package/
   Method: POST
   Content type: json
```
The request expect a body of type ```form```, with the following keys.
1. name : The name of the master package.
2. description : The description for the master package.
3. uninstall_file: A File which will be used to uninstall earlier version of template file, while adding new versions.
4. pre_script_file: This file should contain env setup instructions which have to be called before a template file is installed.
5. post_script_files: This file should contain env cleanup instruction which have to be called after a template file is installed.

Here are a list of optional parameters that can be set for the master package. These parameters are set as default for the template files in the package, when the package is generated, if the template entity do not have these parameters.
1. path : The folder where the template file is to be stored.
2. user : The user which should own the template file.
3. group : The group which should own the template file.
4. permission : The permissions set for the template file.

The API responds with the following json content, when it is able to create a master package. The response code/status is 200.

```json
{
    "message": "Master Package added"
}
```
You can find the master package id using the retrieve API

### Retrieve
This API is used to fetch a list of available master package entities present in the database. The details of the API are as follows

```
   URL: /api/v1.0/master_package/
   Method: GET
   Content type: json
```
The API does not take any request params, and just retuns back with a list of available master package entities. Each entry in the list contains the master package id, name, description and active status of the entitiy.

The API responds with the following json content, when it is able update the version. The response code/status is 200.

```json
{
    "data": [
        {
            "id": <master_id>,
            "name": "<master name>",
            "description": "<master description>",
            "status":<master status>
        }
    ]
}
```

### Update
This API is used to update the master package. The details of the API are as follows

```
   URL: /api/v1.0/master_package/<int:master_id>/
   Method: POST
   Content type: json
```
The master id field in the url, is the id of the master package entitiy which would be update.

The request expect a body of type form-data, with the same set of keys as the create API, with the difference that all keys are optional, and would be upated if present

The API responds with the following json content, when it is able update the version. The response code/status is 200.

```json
{
    "message": "Master Package updated"
}
```

### Assign
This API is used to assign/map the master package to a given edge type and edge subtype conbination.
The details of the API are as follows


```
   URL: /api/v1.0/master_package/assign/<int:master_id>/
   Method: POST
   Content type: json
```
The master id field in the url, is the id of the master package entitiy which you want to assign to the edge type/sub type.

The request expect a body of type json, with the following content.

```json
{
	"edge_type": "<edge_type>",
	"edge_sub_type": "<edge_sub_type>"
}
```

The allowed combination of edge type and subtype are as per the following table.

Type | Sub Type 
--- | --- 
static | default
mid | default
mobile | default
mobile | kontronmetro
mobile | c2cbus
mid | parent_pseudo_tp
mid | child_pseudo_tp
static | nuc
static | ct_static
mobile | railtel_pilot_ec

The API responds with the following json content, when it is able update the version. The response code/status is 200.

```json
{
    "message": "Package assigned"
}
```

### Unassign
This API is used to unassign/unmap the master package from a given edge type and edge subtype conbination.
The details of the API are as follows


```
   URL: /api/v1.0/master_package/assign/<int:master_id>/
   Method: DELETE
   Content type: json
```
The master id field in the url, is the id of the master package entitiy which you want to unassign from the edge type/sub type.

The request expect a body of type json, with the following content.

```json
{
	"edge_type": "<edge_type>",
	"edge_sub_type": "<edge_sub_type>"
}
```

The allowed combination of edge type and subtype are as per the following table.

Type | Sub Type 
--- | --- 
static | default
mid | default
mobile | default
mobile | kontronmetro
mobile | c2cbus
mid | parent_pseudo_tp
mid | child_pseudo_tp
static | nuc
static | ct_static
mobile | railtel_pilot_ec

If the package was earlier assigned to the edge type, then the API unassigns the package and returns a response code/status of 200, with the following response.
```json
{
    "message": "Package deleted"
}
```

### Delete master package

This is a misnomer. While the API is called "Delete master package" ,the API simply sets the status of the master package to 0, and sets all the template files assigned to the master package to be uninstalled.

The details of the API are as follows


```
   URL: /api/v1.0/master_package/<int:master_id>/
   Method: DELETE
   Content type: json
```

Where master_id is the id of the master package whose status has to be set to 0.

The API does not expect any parameters of any sort, and will responsd with a code/status 200, and response as follows

```json
{
    "message": "Master Package deleted"
}
```

## Template set API

The provisioning store, provides template set API for edge devices. The API allow edge devices to get details on, generate packages and find the url where they can download the generated package.
These API make calls to the IPAM and DP server to get details of the edge devices, before responding to the API calls.

The API provided by the provisioning store, to the edge devices are as follows.

### Retrieve template set
This API allows an edge device to get details of the master packages assigned to it, and also the template version assigned to each master package.

The details of the API are as follows

```
   URL: /api/v1.0/template_set/latest
   Method: GET
   Content type: json
```

The API requires the following 2 url parameters
1. edge_id: This is the id of the edge, which is requesting the information. This is a required parameter.
2. set_version: This is the version of the template files set on the edge device. This is an optional parameter.

The API checks which is the latest version of the different template files that have to be installed onto the device. If the device does not require an udpated (inferred from the set_version parameter), then the API informs the edge accordingly.

The API responds with a response code/staus of 200, with the following response content.

```json
{
    "data": [ <master package list>],
    "latest_set_version": "<latest version number>"
}
```

Each master package entry in the data, is of the following format.

```json
{
    "name": "<name of the master package>",
    "description": "<master package description>",
    "status": <master status>,
    "execution_sequence": <execution sequence number>,
    "master_package_id": <master_id,
    "config_template": [ <assigned templates>]
}
```
Each assigned template is of the following format

```json
{
    "name": "<template name>",
    "description": "<template description>",
    "path": "<template path>",
    "owner": "<template owner>",
    "group": "<template owner group>",
    "permissions": <template permissions>,
    "template_id": <template id>,
    "latest_version": {
        "version_no": "<template version>",
        "comment": "<template version comment>"
    }
}
```

### Generate package.

This API allows the edge devices to inform the provisioning store to generate a tar package for it to download.
The details of the API are as follows.

```
   URL: /api/v1.0/config_package
   Method: GET
   Content type: json
```


The API requires the following 2 url parameters
1. mac_address: This is a '|' separated list of mac addresses of the different interfaces of the edge. This is an optional parameter
1. edge_id: This is the id of the edge, which is requesting the information. This is an optional parameter, but becomes required if mac address is not passed.
2. set_version: This is the version of the template files set on the edge device. This is an optional parameter.

The API makes the required calls to the IPAM and DP server, accordingly generates the required tar package for the edge device.

On successful generation of the tar, the API responds with the follwoing response and a response code/status of 200.

```json
{
    "data": "Package generated",
    "path": "<url to download the package>",
    "edge_id": "<edge id>",
    "latest_set_version": "<version of the package provided"
}
```

**NOTE**: The url provided by the response is not an API that the provisioning store provides. You have to use a different mechanism to provide the tar package.

## Telemetry API

The provisioning store provides telemetry API which allow edge devices to inform the provisioning store that a specific package has been downloaded and installed. The telemetry API can also be used by admins to get reports on the download and usage of different config packages.

### Package Download status.

This API allows edge devices to inform the provisioning store, that it has downloaded a package. The API call can only happen from static or mid devices. mobile devices have to make the call by using mid devices as a proxy.

As such this API requires the ```x-forwarded-for``` header to be set.

The details of the API as follows

```
   URL: /api/v1.0/edge_telemetry/package_download/<proxy_edge_id>/status/
   Method: POST
   Content type: json
```
In the above url, the proxy_edge_id refers to the devices which is used as the source or the proxy, and can only be the mid or static edge type.

The status can be success for success, and anything else for failure.

The API expects the following json data in the body

```json
{
	"edge_id": "<reporting_edge_id>",
	"package_name": "<downloaded package>",
	"template_set_version": "<package version>"
}
```

The API responds with a 200 response code/status regardless of whether url parameter status was success or not.

When the url parameter status is set to success, the API responds with the following response

```json
{
    "message": "success",
    "description": "Package Download Successful"
}
```
For a status set to anything other than success, the response is

```json
{
    "message": "success",
    "description": "Package Download Failed"
}
```

### Package Consumption status.
This API is the same as the above API, with the difference that it is used to inform the provisioning store on whether the downloaded config package was properly installed or not.

The details of the API are as follows

The details of the API as follows

```
   URL: /api/v1.0/edge_telemetry/package_consumption/<proxy_edge_id>/status/
   Method: POST
   Content type: json
```
In the above url, the proxy_edge_id refers to the devices which is used as the source or the proxy, and can only be the mid or static edge type.

The status can be success for success, and anything else for failure.

The API expects the following json data in the body

```json
{
	"edge_id": "<reporting_edge_id>",
	"package_name": "<downloaded package>",
	"template_set_version": "<package version>"
}
```

The API responds with a 200 response code/status regardless of whether url parameter status was success or not.

When the url parameter status is set to success, the API responds with the following response

```json
{
    "message": "success",
    "description": "Package Consumption Successful"
}
```
For a status set to anything other than success, the response is

```json
{
    "message": "success",
    "description": "Package Consumption Failed"
}
```

### Reportee Edge List

This API can be used by an Admin to get a list of Edge ids of the edge devices which have sent telemetry data to the provisioning store.

The details of the API are as follows:
```
   URL: /api/v1.0/edge_telemetry/report_list/
   Method: GET
   Content type: json
```

The API does not take any url parameters or any special headers.

The API responds with response code/status 200, and a response of the following format.

```json
{
    "data": {
        "edge_id_list": [ <edge id list>]
    }
}
```

Where edge id list, is a list of edge ids that have either reported package download status, or package consumption status to the provisioning store.

### Retrieve Edge info.

This API can be used by an Admin to get a list of packages and their download and consumption status, as reported by the supplied edge id.

The details of the API are as follows:
```
   URL: /api/v1.0/edge_telemetry/report/<edge_id>
   Method: GET
   Content type: json
```

The API does not expect any url parameters. The edge id in the url refers to the id of the edge, whose package download and consumption status has been reqeusted.

The API responds with a response code/status of 200, and the following format for response.

```json
{
    "data": [<telemetry data object>]
}
```

The data list contains telemetry data objects of the format

```json
{
    "edge_id": "<reporting edge id>",
    "package_name": "<reporded package name>",
    "report": {
        "downloaded": {
            "success": <download status in boolean>,
            "date_time": "<reporting time if download status was successful>"
        },
        "consumed": {
            "success": <install status in boolean>,
            "date_time": "<reporting time if install status was successful>"
        }
    },
    "template_set_version": "<version of the installed package>"
}
```

### Report info list.

This API provides a paginated list of edge id reports. The list contains only the report for the latest package version for which an edge id has sent the download or install status to the provisioning store. The list contains only 1 report object for each edge id.

The page size is by default 20, as in the API will return a maximum of 20 report every time it is called.

The details of the API are as follows:
```
   URL: /api/v1.0/edge_telemetry_info_list/report/<page_number>/
   Method: GET
   Content type: json
```

The API does not expect any url parameters. The page number refers to which report page should be retrieved from the provisioning store. The returned list is sorted as per edge ids, according to the when each edge id first reported download or consumption status.

The API responds with a response code/status of 200, and the following format for response.

```json
{
    "meta": {
        "code": 200,
        "timestamp": "<The timestamp at which the API was called>"
    },
    "data": [<telemetry data object>],
    "pagination": {
        "total": <number of edge ids that reported status>,
        "page": <current page number>,
        "per_page": 20
    }
}
```

The data list contains telemetry data objects of the format

```json
{
    "edge_id": "<reportee edge id>",
    "package_name": "<package name>",
    "template_set_version": "<package version>",
    "ip_address": "<reportee ip address as per forwarded header>",
    "consumed": <install status in boolean>,
    "downloaded": <download status in boolean>,
    "downloaded_time": <download timestamp if success>,
    "consumed_time": <install timestamp if success>
}
```

### Info report

This API is very similar to the ```Report Info List``` API, but provides data for only 1 edge id at a time.

The details of the url are as follows

The details of the API are as follows:
```
   URL: /api/v1.0/edge_telemetry_info/report/<edge id>/
   Method: GET
   Content type: json
```

The API does not expect any url parameters. The edge id refers to the id of the edge device for which the report is requested.

The API responds with a response code/status of 200, and the following format for response.

```json
{
    "meta": {
        "code": 200,
        "timestamp": "<The timestamp at which the API was called>"
    },
    "data": 
    {
        "edge_id": "<reportee edge id>",
        "package_name": "<package name>",
        "template_set_version": "<package version>",
        "ip_address": "<reportee ip address as per forwarded header>",
        "consumed": <install status in boolean>,
        "downloaded": <download status in boolean>,
        "downloaded_time": <download timestamp if success>,
        "consumed_time": <install timestamp if success>
    }
}
```
