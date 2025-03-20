# (C) Copyright 2019-2025 Hewlett Packard Enterprise Development LP.
# Apache License 2.0

from pyhpesse.common import (
    _generate_parameterised_url,
    _remove_empty_keys,
    HPESecureServiceEdgeApiLogin,
)

# FileName: adminapi.py

class AdminApi(HPESecureServiceEdgeApiLogin):

    # API Service - ApplicationGroups
    def new_applicationgroups(self, body):
        """
        Operation: Create a New Application Group

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "applications": "[string]",
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/Tags"
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="post")

    # API Service - ApplicationGroups
    def get_applicationgroups(self, pagenumber, pagesize):
        """
        Operation: Get Application Groups

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: pagenumber, Required: Optional, Type: integer, Description: none supplied

        Parameter Name: pagesize, Required: Optional, Type: integer, Description: none supplied

        """
        url_path = "/api/v1.0/Tags"
        dict_query ={'pagenumber': pagenumber, 'pagesize': pagesize}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - ApplicationGroups
    def update_applicationgroups(self, id, body):
        """
        Operation: Update an Existing Application Group

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "applications": "[string]",
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/Tags/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="put")

    # API Service - ApplicationGroups
    def delete_applicationgroups(self, id):
        """
        Operation: Delete Application Group by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/Tags/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="delete")

    # API Service - ApplicationGroups
    def getbyid_applicationgroups(self, id):
        """
        Operation: Get Application Group by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/Tags/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - Applications
    def new_applications(self, body):
        """
        Operation: Create a New Application

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "enabled": True/False,
            "connectorZoneId": "string",
            "tags": "[string]",
            "identityProviderId": "string",
            "networkRangeApplicationData": {
                "dnsSearches": "[string]",
                "ipRangesOrCIDRs": "[string]",
                "excludedDnsSearches": "[string]",
                "portsAndProtocols": "[string]",
                "enableIcmp": True/False,
                "serverInitiatedPorts": "[string]",
                "enforceResolvedDnsToIp": True/False
            },
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/Applications"
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="post")

    # API Service - Applications
    def get_applications(self, pagenumber, pagesize):
        """
        Operation: Get Applications

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: pagenumber, Required: Optional, Type: integer, Description: none supplied

        Parameter Name: pagesize, Required: Optional, Type: integer, Description: none supplied

        """
        url_path = "/api/v1.0/Applications"
        dict_query ={'pagenumber': pagenumber, 'pagesize': pagesize}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - Applications
    def update_applications(self, id, body):
        """
        Operation: Update an Existing Application

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "enabled": True/False,
            "connectorZoneId": "string",
            "tags": "[string]",
            "identityProviderId": "string",
            "networkRangeApplicationData": {
                "dnsSearches": "[string]",
                "ipRangesOrCIDRs": "[string]",
                "excludedDnsSearches": "[string]",
                "portsAndProtocols": "[string]",
                "enableIcmp": True/False,
                "serverInitiatedPorts": "[string]",
                "enforceResolvedDnsToIp": True/False
            },
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/Applications/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="put")

    # API Service - Applications
    def getbyid_applications(self, id):
        """
        Operation: Get Application by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/Applications/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - Applications
    def delete_applications(self, id):
        """
        Operation: Delete Application by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/Applications/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="delete")

    # API Service - Commit
    def commit_commitchanges(self):
        """
        Operation: Commit Changes

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        """
        url_path = "/api/v1.0/Commit"
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="post")

    # API Service - Connectors
    def new_connectors(self, body):
        """
        Operation: Create a New Connector

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "enabled": True/False,
            "connectorZoneId": "string",
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/Connectors"
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="post")

    # API Service - Connectors
    def get_connectors(self, pagenumber, pagesize):
        """
        Operation: Get Connectors

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: pagenumber, Required: Optional, Type: integer, Description: none supplied

        Parameter Name: pagesize, Required: Optional, Type: integer, Description: none supplied

        """
        url_path = "/api/v1.0/Connectors"
        dict_query ={'pagenumber': pagenumber, 'pagesize': pagesize}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - Connectors
    def update_connectors(self, id, body):
        """
        Operation: Update an Existing Connector

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "enabled": True/False,
            "connectorZoneId": "string",
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/Connectors/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="put")

    # API Service - Connectors
    def getbyid_connectors(self, id):
        """
        Operation: Get Connector by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/Connectors/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - Connectors
    def delete_connectors(self, id):
        """
        Operation: Delete Connector by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/Connectors/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="delete")

    # API Service - Connectors
    def regenerate_connectors(self, id):
        """
        Operation: Regenerate an Installation Command for an Exisitng Connector

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/Connectors/{id}/regenerate"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="post")

    # API Service - Connectors
    def status_connectors(self, id):
        """
        Operation: Get the Status of a Connector

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/Connectors/{id}/status"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - ConnectorZones
    def new_connectorzones(self, body):
        """
        Operation: Create a New Connector Zone

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "connectors": "[string]",
            "description": "string",
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/ConnectorZones"
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="post")

    # API Service - ConnectorZones
    def get_connectorzones(self, pagenumber, pagesize):
        """
        Operation: Get Connector Zones

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: pagenumber, Required: Optional, Type: integer, Description: none supplied

        Parameter Name: pagesize, Required: Optional, Type: integer, Description: none supplied

        """
        url_path = "/api/v1.0/ConnectorZones"
        dict_query ={'pagenumber': pagenumber, 'pagesize': pagesize}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - ConnectorZones
    def update_connectorzones(self, id, body):
        """
        Operation: Update an Existing Connector Zone

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "connectors": "[string]",
            "description": "string",
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/ConnectorZones/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="put")

    # API Service - ConnectorZones
    def getbyid_connectorzones(self, id):
        """
        Operation: Get Connector Zone by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/ConnectorZones/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - ConnectorZones
    def delete_connectorzones(self, id):
        """
        Operation: Delete Connector Zone by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/ConnectorZones/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="delete")

    # API Service - CustomIpCategory
    def new_customipcategory(self, body):
        """
        Operation: Create a New IP Category

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "includedIps": [
                "string"
            ],
            "excludedIps": [
                "string"
            ],
            "connectorZoneId": "string",
            "description": "string",
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/IpCategories"
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="post")

    # API Service - CustomIpCategory
    def get_customipcategory(self, pagenumber, pagesize):
        """
        Operation: Get IP Categories

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: pagenumber, Required: Optional, Type: integer, Description: none supplied

        Parameter Name: pagesize, Required: Optional, Type: integer, Description: none supplied

        """
        url_path = "/api/v1.0/IpCategories"
        dict_query ={'pagenumber': pagenumber, 'pagesize': pagesize}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - CustomIpCategory
    def update_customipcategory(self, id, body):
        """
        Operation: Update an Existing IP Category

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "includedIps": [
                "string"
            ],
            "excludedIps": [
                "string"
            ],
            "connectorZoneId": "string",
            "description": "string",
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/IpCategories/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="put")

    # API Service - CustomIpCategory
    def getbyid_customipcategory(self, id):
        """
        Operation: Get IP Category by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/IpCategories/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - CustomIpCategory
    def delete_customipcategory(self, id):
        """
        Operation: Delete IP Category by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/IpCategories/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="delete")

    # API Service - Groups
    def new_groups(self, body):
        """
        Operation: Create a New Group

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "users": "[string]",
            "description": "string",
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/Groups"
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="post")

    # API Service - Groups
    def get_groups(self, pagenumber, pagesize):
        """
        Operation: Get Groups

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: pagenumber, Required: Optional, Type: integer, Description: none supplied

        Parameter Name: pagesize, Required: Optional, Type: integer, Description: none supplied

        """
        url_path = "/api/v1.0/Groups"
        dict_query ={'pagenumber': pagenumber, 'pagesize': pagesize}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - Groups
    def update_groups(self, id, body):
        """
        Operation: Update an Existing Group

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "users": "[string]",
            "description": "string",
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/Groups/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="put")

    # API Service - Groups
    def getbyid_groups(self, id):
        """
        Operation: Get Group by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/Groups/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - Groups
    def delete_groups(self, id):
        """
        Operation: Delete Group by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/Groups/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="delete")

    # API Service - IpFeedCategory
    def new_ipfeedcategory(self, body):
        """
        Operation: Create a New IP Category

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "includedIps": [
                "string"
            ],
            "excludedIps": [
                "string"
            ],
            "connectorZoneId": "string",
            "description": "string",
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/IpCategoriesFeed"
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="post")

    # API Service - IpFeedCategory
    def get_ipfeedcategory(self, pagenumber, pagesize):
        """
        Operation: Get IP Categories

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: pagenumber, Required: Optional, Type: integer, Description: none supplied

        Parameter Name: pagesize, Required: Optional, Type: integer, Description: none supplied

        """
        url_path = "/api/v1.0/IpCategoriesFeed"
        dict_query ={'pagenumber': pagenumber, 'pagesize': pagesize}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - IpFeedCategory
    def update_ipfeedcategory(self, id, body):
        """
        Operation: Update an Existing IP Category

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "includedIps": [
                "string"
            ],
            "excludedIps": [
                "string"
            ],
            "connectorZoneId": "string",
            "description": "string",
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/IpCategoriesFeed/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="put")

    # API Service - IpFeedCategory
    def getbyid_ipfeedcategory(self, id):
        """
        Operation: Get IP Category by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/IpCategoriesFeed/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - IpFeedCategory
    def delete_ipfeedcategory(self, id):
        """
        Operation: Delete IP Category by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/IpCategoriesFeed/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="delete")

    # API Service - Locations
    def new_locations(self, body):
        """
        Operation: Create a New Location

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "subLocations": "[string]",
            "tunnels": "[string]",
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/Locations"
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="post")

    # API Service - Locations
    def get_locations(self, pagenumber, pagesize):
        """
        Operation: Get Locations

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: pagenumber, Required: Optional, Type: integer, Description: none supplied

        Parameter Name: pagesize, Required: Optional, Type: integer, Description: none supplied

        """
        url_path = "/api/v1.0/Locations"
        dict_query ={'pagenumber': pagenumber, 'pagesize': pagesize}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - Locations
    def getbyid_locations(self, id):
        """
        Operation: Get Location by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/Locations/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - Locations
    def delete_locations(self, id):
        """
        Operation: Delete Location by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/Locations/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="delete")

    # API Service - Locations
    def update_locations(self, id, body):
        """
        Operation: Update an Existing Location

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "subLocations": "[string]",
            "tunnels": "[string]",
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/Locations/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="put")

    # API Service - SslExclusions
    def new_sslexclusions(self, body):
        """
        Operation: Create a New SSL Exclusion

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "enabled": True/False,
            "excludedDomains": [
                "string"
            ],
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/SslExclusions"
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="post")

    # API Service - SslExclusions
    def get_sslexclusions(self, pagenumber, pagesize):
        """
        Operation: Get SSL Exclusions

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: pagenumber, Required: Optional, Type: integer, Description: none supplied

        Parameter Name: pagesize, Required: Optional, Type: integer, Description: none supplied

        """
        url_path = "/api/v1.0/SslExclusions"
        dict_query ={'pagenumber': pagenumber, 'pagesize': pagesize}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - SslExclusions
    def update_sslexclusions(self, id, body):
        """
        Operation: Update an Existing SSL Exclusion

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "enabled": True/False,
            "excludedDomains": [
                "string"
            ],
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/SslExclusions/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="put")

    # API Service - SslExclusions
    def getbyid_sslexclusions(self, id):
        """
        Operation: Get SSL Exclusion by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/SslExclusions/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - SslExclusions
    def delete_sslexclusions(self, id):
        """
        Operation: Delete SSL Exclusion by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/SslExclusions/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="delete")

    # API Service - SubLocations
    def new_sublocations(self, locationid, body):
        """
        Operation: Create a New SubLocation

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: locationid, Required: Mandatory, Type: string, Description: none supplied

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "ipRanges": [
                "string"
            ],
            "locationId": "string",
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/Locations/{locationId}/SubLocations"
        dict_path = {'locationid': locationid}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="post")

    # API Service - SubLocations
    def get_sublocations(self, locationid, pagenumber, pagesize):
        """
        Operation: Get SubLocations

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: locationid, Required: Mandatory, Type: string, Description: none supplied

        Parameter Name: pagenumber, Required: Optional, Type: integer, Description: none supplied

        Parameter Name: pagesize, Required: Optional, Type: integer, Description: none supplied

        """
        url_path = "/api/v1.0/Locations/{locationId}/SubLocations"
        dict_path = {'locationid': locationid}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - SubLocations
    def getbyid_sublocations(self, locationid, id):
        """
        Operation: Get SubLocation by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: locationid, Required: Mandatory, Type: string, Description: none supplied

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/Locations/{locationId}/SubLocations/{id}"
        dict_path = {'locationid': locationid, 'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - SubLocations
    def delete_sublocations(self, locationid, id):
        """
        Operation: Delete SubLocation by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: locationid, Required: Mandatory, Type: string, Description: none supplied

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/Locations/{locationId}/SubLocations/{id}"
        dict_path = {'locationid': locationid, 'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="delete")

    # API Service - SubLocations
    def update_sublocations(self, locationid, id, body):
        """
        Operation: Update an Existing SubLocation

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: locationid, Required: Mandatory, Type: string, Description: none supplied

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "ipRanges": [
                "string"
            ],
            "locationId": "string",
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/Locations/{locationId}/SubLocations/{id}"
        dict_path = {'locationid': locationid, 'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="put")

    # API Service - Tunnels
    def new_tunnels(self, body):
        """
        Operation: Create a New Tunnel

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "authenticationID": "string",
            "authenticationPsk": "string",
            "locationID": "string",
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/Tunnels"
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="post")

    # API Service - Tunnels
    def get_tunnels(self, pagenumber, pagesize):
        """
        Operation: Get Tunnels

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: pagenumber, Required: Optional, Type: integer, Description: none supplied

        Parameter Name: pagesize, Required: Optional, Type: integer, Description: none supplied

        """
        url_path = "/api/v1.0/Tunnels"
        dict_query ={'pagenumber': pagenumber, 'pagesize': pagesize}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - Tunnels
    def getbyid_tunnels(self, id):
        """
        Operation: Get Tunnel by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/Tunnels/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - Tunnels
    def delete_tunnels(self, id):
        """
        Operation: Delete Tunnel by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/Tunnels/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="delete")

    # API Service - Tunnels
    def update_tunnels(self, id, body):
        """
        Operation: Update an Existing Tunnel

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "authenticationID": "string",
            "authenticationPsk": "string",
            "locationID": "string",
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/Tunnels/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="put")

    # API Service - Tunnels
    def status_tunnels(self, id):
        """
        Operation: Get the Status of a Tunnel

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/Tunnels/{id}/status"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - Users
    def new_users(self, body):
        """
        Operation: Create a New User

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "userName": "string",
            "email": "string",
            "firstName": "string",
            "lastName": "string",
            "enabled": True/False,
            "expiration": "string",
            "groups": "[string]",
            "sshPrivateKey": "string",
            "hasSshPrivateKey": True/False
        }
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/Users"
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="post")

    # API Service - Users
    def get_users(self, pagenumber, pagesize):
        """
        Operation: Get Users

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: pagenumber, Required: Optional, Type: integer, Description: none supplied

        Parameter Name: pagesize, Required: Optional, Type: integer, Description: none supplied

        """
        url_path = "/api/v1.0/Users"
        dict_query ={'pagenumber': pagenumber, 'pagesize': pagesize}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - Users
    def update_users(self, id, body):
        """
        Operation: Update an Existing User

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "userName": "string",
            "email": "string",
            "firstName": "string",
            "lastName": "string",
            "enabled": True/False,
            "expiration": "string",
            "groups": "[string]",
            "sshPrivateKey": "string",
            "hasSshPrivateKey": True/False
        }
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/Users/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="put")

    # API Service - Users
    def getbyid_users(self, id):
        """
        Operation: Get User by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/Users/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - Users
    def delete_users(self, id):
        """
        Operation: Delete User by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/Users/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="delete")

    # API Service - WebCategory
    def new_webcategory(self, body):
        """
        Operation: Create a New Web Category

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "includedDomainsOrUrls": [
                "string"
            ],
            "excludedDomainsOrUrls": [
                "string"
            ],
            "connectorZoneId": "string",
            "description": "string",
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/WebCategories"
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="post")

    # API Service - WebCategory
    def get_webcategory(self, pagenumber, pagesize):
        """
        Operation: Get Web Categories

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: pagenumber, Required: Optional, Type: integer, Description: none supplied

        Parameter Name: pagesize, Required: Optional, Type: integer, Description: none supplied

        """
        url_path = "/api/v1.0/WebCategories"
        dict_query ={'pagenumber': pagenumber, 'pagesize': pagesize}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - WebCategory
    def update_webcategory(self, id, body):
        """
        Operation: Update an Existing Web Category

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        
        Available Body Parameters:
        body={
            "includedDomainsOrUrls": [
                "string"
            ],
            "excludedDomainsOrUrls": [
                "string"
            ],
            "connectorZoneId": "string",
            "description": "string",
            "name": "string",
            "id": "string"
        }

        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/api/v1.0/WebCategories/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        body = _remove_empty_keys(keys=body)
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, query=body, method="put")

    # API Service - WebCategory
    def getbyid_webcategory(self, id):
        """
        Operation: Get Web Category by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/WebCategories/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="get")

    # API Service - WebCategory
    def delete_webcategory(self, id):
        """
        Operation: Delete Web Category by ID

        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self

        Parameter Name: id, Required: Mandatory, Type: string, Description: none supplied

        """
        url_path = "/api/v1.0/WebCategories/{id}"
        dict_path = {'id': id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPESecureServiceEdgeApiLogin._send_request(self, url=url_path, method="delete")
