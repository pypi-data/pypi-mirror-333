# (C) Copyright 2019-2025 Hewlett Packard Enterprise Development LP.
# Apache License 2.0

from pyhpeuxi.common import (
    _generate_parameterised_url,
    _remove_empty_keys,
    HPEUXIApiLogin,
)

# FileName: openapi.py


class OpenApi(HPEUXIApiLogin):

    # API Service : agents
    def delete_agent(self, id):
        """
        Operation: Agent Delete
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: id, Required: Mandatory, Type: string, Description: the unique identifier of the agent
        """
        url_path = "/networking-uxi/v1alpha1/agents/{id}"
        dict_path = {"id": id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPEUXIApiLogin._send_request(self, url=url_path, method="delete")

    # API Service : agents
    def update_agent(self, id, body):
        """
        Operation: Agent Patch
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: id, Required: Mandatory, Type: string, Description: the unique identifier of the agent
        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        Available Body Parameters:

        body={
            'name' : 'string', # The name of the agent
            'notes' : 'string', # The notes of the agent
            'pcapMode' : 'string', # Options are: ['light', 'full', 'off']
        }
        Mandatory Body Parameters:
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/networking-uxi/v1alpha1/agents/{id}"
        dict_path = {"id": id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        body = _remove_empty_keys(keys=body)
        return HPEUXIApiLogin._send_request(
            self, url=url_path, query=body, method="patch"
        )

    # API Service : agent-group-assignments
    def delete_group_agent(self, id):
        """
        Operation: Agent Group Assignment Delete
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: id, Required: Mandatory, Type: string, Description: the unique identifier of the assignment
        """
        url_path = "/networking-uxi/v1alpha1/agent-group-assignments/{id}"
        dict_path = {"id": id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPEUXIApiLogin._send_request(self, url=url_path, method="delete")

    # API Service : agent-group-assignments
    def new_group_agent(self, body):
        """
        Operation: Agent Group Assignment Post
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        Available Body Parameters:

        body={
            'groupId' : 'string', # The unique identifier of the group
            'agentId' : 'string', # The unique identifier of the agent
        }
        Mandatory Body Parameters: groupId, agentId
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/networking-uxi/v1alpha1/agent-group-assignments"
        body = _remove_empty_keys(keys=body)
        return HPEUXIApiLogin._send_request(
            self, url=url_path, query=body, method="post"
        )

    # API Service : agent-group-assignments
    def get_group_agent(self, id=""):
        """
        Operation: Agent Group Assignments Get
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: id, Required: Optional, Type: string, Description: the id of the resource.
        """
        url_path = "/networking-uxi/v1alpha1/agent-group-assignments"
        dict_query = {"id": id}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPEUXIApiLogin._send_request(self, url=url_path, method="get")

    # API Service : agents
    def get_agents(self, id=""):
        """
        Operation: Agents Get
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: id, Required: Optional, Type: string, Description: the id of the resource.
        """
        url_path = "/networking-uxi/v1alpha1/agents"
        dict_query = {"id": id}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPEUXIApiLogin._send_request(self, url=url_path, method="get")

    # API Service : groups
    def delete_group(self, id):
        """
        Operation: Group Delete
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: id, Required: Mandatory, Type: string, Description: the unique identifier of the group.
        """
        url_path = "/networking-uxi/v1alpha1/groups/{id}"
        dict_path = {"id": id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPEUXIApiLogin._send_request(self, url=url_path, method="delete")

    # API Service : groups
    def update_group(self, id, body):
        """
        Operation: Group Patch
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: id, Required: Mandatory, Type: string, Description: the unique identifier of the group
        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        Available Body Parameters:

        body={
            'name' : 'string', # The updated group name
        }
        Mandatory Body Parameters:
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/networking-uxi/v1alpha1/groups/{id}"
        dict_path = {"id": id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        body = _remove_empty_keys(keys=body)
        return HPEUXIApiLogin._send_request(
            self, url=url_path, query=body, method="patch"
        )

    # API Service : groups
    def new_new_group(self, body):
        """
        Operation: Group Post
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        Available Body Parameters:

        body={
            'parentId' : 'string', # The unique identifier of the parent group
            'name' : 'string', # The name of the group
        }
        Mandatory Body Parameters: name
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/networking-uxi/v1alpha1/groups"
        body = _remove_empty_keys(keys=body)
        return HPEUXIApiLogin._send_request(
            self, url=url_path, query=body, method="post"
        )

    # API Service : groups
    def get_groups(self, id=""):
        """
        Operation: Groups Get
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: id, Required: Optional, Type: string, Description: the id of the resource.
        """
        url_path = "/networking-uxi/v1alpha1/groups"
        dict_query = {"id": id}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPEUXIApiLogin._send_request(self, url=url_path, method="get")

    # API Service : network-group-assignments
    def delete_group_network(self, id):
        """
        Operation: Network Group Assignment Delete
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: id, Required: Mandatory, Type: string, Description: the unique identifier of the network group assignment
        """
        url_path = "/networking-uxi/v1alpha1/network-group-assignments/{id}"
        dict_path = {"id": id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPEUXIApiLogin._send_request(self, url=url_path, method="delete")

    # API Service : network-group-assignments
    def new_group_network(self, body):
        """
        Operation: Network Group Assignment Post
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        Available Body Parameters:

        body={
            'groupId' : 'string', # The unique identifier of the group
            'networkId' : 'string', # The unique identifier of the network
        }
        Mandatory Body Parameters: groupId, networkId
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/networking-uxi/v1alpha1/network-group-assignments"
        body = _remove_empty_keys(keys=body)
        return HPEUXIApiLogin._send_request(
            self, url=url_path, query=body, method="post"
        )

    # API Service : network-group-assignments
    def get_group_network(self, id=""):
        """
        Operation: Network Group Assignments Get
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: id, Required: Optional, Type: string, Description: the id of the resource.
        """
        url_path = "/networking-uxi/v1alpha1/network-group-assignments"
        dict_query = {"id": id}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPEUXIApiLogin._send_request(self, url=url_path, method="get")

    # API Service : sensor-group-assignments
    def delete_group_sensor(self, id):
        """
        Operation: Sensor Group Assignment Delete
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: id, Required: Mandatory, Type: string, Description: the unique identifier of the sensor group assignment
        """
        url_path = "/networking-uxi/v1alpha1/sensor-group-assignments/{id}"
        dict_path = {"id": id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPEUXIApiLogin._send_request(self, url=url_path, method="delete")

    # API Service : sensor-group-assignments
    def new_group_sensor(self, body):
        """
        Operation: Sensor Group Assignment Post
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        Available Body Parameters:

        body={
            'groupId' : 'string', # The unique identifier of the group
            'sensorId' : 'string', # The unique identifier of the sensor
        }
        Mandatory Body Parameters: groupId, sensorId
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/networking-uxi/v1alpha1/sensor-group-assignments"
        body = _remove_empty_keys(keys=body)
        return HPEUXIApiLogin._send_request(
            self, url=url_path, query=body, method="post"
        )

    # API Service : sensor-group-assignments
    def get_group_sensor(self, id=""):
        """
        Operation: Sensor Group Assignments Get
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: id, Required: Optional, Type: string, Description: the id of the resource.
        """
        url_path = "/networking-uxi/v1alpha1/sensor-group-assignments"
        dict_query = {"id": id}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPEUXIApiLogin._send_request(self, url=url_path, method="get")

    # API Service : sensors
    def update_sensor(self, id, body):
        """
        Operation: Sensor Patch
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: id, Required: Mandatory, Type: string, Description: the unique identifier of the sensor
        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        Available Body Parameters:

        body={
            'name' : 'string', # The updated sensor name
            'addressNote' : 'string', # The updated address note for the sensor
            'notes' : 'string', # Additional notes for the sensor
            'pcapMode' : 'string', # Options are: ['light', 'full', 'off']
        }
        Mandatory Body Parameters:
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/networking-uxi/v1alpha1/sensors/{id}"
        dict_path = {"id": id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        body = _remove_empty_keys(keys=body)
        return HPEUXIApiLogin._send_request(
            self, url=url_path, query=body, method="patch"
        )

    # API Service : sensors
    def get_sensors(self, id=""):
        """
        Operation: Sensors Get
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: id, Required: Optional, Type: string, Description: the id of the resource.
        """
        url_path = "/networking-uxi/v1alpha1/sensors"
        dict_query = {"id": id}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPEUXIApiLogin._send_request(self, url=url_path, method="get")

    # API Service : service-test-group-assignments
    def delete_test_service(self, id):
        """
        Operation: Service Test Group Assignment Delete
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: id, Required: Mandatory, Type: string, Description: the unique identifier of the service test group assignment
        """
        url_path = "/networking-uxi/v1alpha1/service-test-group-assignments/{id}"
        dict_path = {"id": id}
        for item in dict_path:
            url_path = url_path.replace("{" + item + "}", dict_path[item])
        return HPEUXIApiLogin._send_request(self, url=url_path, method="delete")

    # API Service : service-test-group-assignments
    def new_test_service(self, body):
        """
        Operation: Service Test Group Assignment Post
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: body, Required: Mandatory, Type: Object, Description: Body Parameters
        Available Body Parameters:

        body={
            'groupId' : 'string', # The unique identifier of the group
            'serviceTestId' : 'string', # The unique identifier of the service test
        }
        Mandatory Body Parameters: groupId, serviceTestId
        """
        if body is None:
            raise ValueError("The 'body' parameter is mandatory and cannot be None.")
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary.")
        url_path = "/networking-uxi/v1alpha1/service-test-group-assignments"
        body = _remove_empty_keys(keys=body)
        return HPEUXIApiLogin._send_request(
            self, url=url_path, query=body, method="post"
        )

    # API Service : service-test-group-assignments
    def get_test_service(self, id=""):
        """
        Operation: Service Test Group Assignments Get
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: id, Required: Optional, Type: string, Description: the id of the resource.
        """
        url_path = "/networking-uxi/v1alpha1/service-test-group-assignments"
        dict_query = {"id": id}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPEUXIApiLogin._send_request(self, url=url_path, method="get")

    # API Service : service-tests
    def get_tests_service(self, id=""):
        """
        Operation: Service Tests Get
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: id, Required: Optional, Type: string, Description: the id of the resource.
        """
        url_path = "/networking-uxi/v1alpha1/service-tests"
        dict_query = {"id": id}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPEUXIApiLogin._send_request(self, url=url_path, method="get")

    # API Service : wired-networks
    def get_networks_wired(self, id=""):
        """
        Operation: Wired Networks Get
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: id, Required: Optional, Type: string, Description: the id of the resource.
        """
        url_path = "/networking-uxi/v1alpha1/wired-networks"
        dict_query = {"id": id}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPEUXIApiLogin._send_request(self, url=url_path, method="get")

    # API Service : wireless-networks
    def get_networks_wireless(self, id=""):
        """
        Operation: Wireless Networks Get
        Parameter Name: login, Required: Mandatory, Type: object, Description: Login Variable associated with self
        Parameter Name: id, Required: Optional, Type: string, Description: the id of the resource.
        """
        url_path = "/networking-uxi/v1alpha1/wireless-networks"
        dict_query = {"id": id}
        url_path = _generate_parameterised_url(parameters=dict_query, url=url_path)
        return HPEUXIApiLogin._send_request(self, url=url_path, method="get")
