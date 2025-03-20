# (C) Copyright 2019-2025 Hewlett Packard Enterprise Development LP.
# Apache License 2.0

import json
import requests
import urllib.parse, urllib3

urllib3.disable_warnings()


class HPESecureServiceEdgeApiLogin:
    def __init__(
        self,
        url="https://admin-api.axissecurity.com",
        api_token="",
        verify_ssl=True,
    ):
        """
        This is the class constructor for HPE Aruba Security Admin API.

        This constructor is required to be created before any modules can be used and must contain the following function arguments:

        Optional Parameters:
        url (string): Website for API Services  - https://admin-api.axissecurity.com
        verify_ssl (boolean): Validate web service cerificate - True/False

        Mandatory Parameters:
        api_token (string): API Token for API Service

        """
        self.url = url
        self.api_token = api_token
        self.verify_ssl = True

    def _send_request(
        self, url, method, query="", content_response_type="application/json"
    ):
        """Sends a request to the Axis Admin API URL
        :query: must contain the json request if model required
        :url: must contain the /url (e.g. /oauth)
        :method: must contain the post or get request type of method
        :content_response_type: by default is set as Application/Json however can be changed by the method if required and functionality exists.
        :api_token optional[]: must contain the api_token for the calls.
        """
        full_url_path = self.url + url

        if len(self.api_token) == 0:
            cred = _new_api_token(self)
            try:
                self.api_token = cred["access_token"]
            except TypeError:
                pass
            except KeyError:
                pass

        if len(self.api_token) != 0:
            header = {
                "Authorization": "Bearer " + self.api_token,
                "accept": content_response_type,
            }
            if method == "post":
                response = requests.post(
                    url=full_url_path,
                    json=query,
                    headers=header,
                    verify=self.verify_ssl,
                )
            if method == "patch":
                response = requests.patch(
                    url=full_url_path,
                    json=query,
                    headers=header,
                    verify=self.verify_ssl,
                )
            if method == "put":
                response = requests.put(
                    url=full_url_path,
                    json=query,
                    headers=header,
                    verify=self.verify_ssl,
                )
            if method == "get":
                response = requests.get(
                    url=full_url_path,
                    json=query,
                    headers=header,
                    verify=self.verify_ssl,
                )
            if method == "delete":
                response = requests.delete(
                    url=full_url_path,
                    json=query,
                    headers=header,
                    verify=self.verify_ssl,
                )
            if method == "":
                print(
                    "method needs to be supplied before sending a request to ClearPass"
                )

            if "json" in content_response_type:
                try:
                    return json.loads(response.text)
                except json.decoder.JSONDecodeError:
                    return response.text
            else:
                return response.content
        else:
            print("Problem logging into HPE SSE Admin API")
            return cred


def _remove_empty_keys(keys):
    remove_empty_values_from_dict = []
    for item in keys:
        if keys[item] == "":
            remove_empty_values_from_dict.append(item)
        else:
            pass
    for removal in remove_empty_values_from_dict:
        del keys[removal]
    return keys


def _generate_parameterised_url(url, parameters=""):
    parameters = _remove_empty_keys(keys=parameters)

    if len(parameters) == 0:
        return url
    else:
        for key, value in parameters.items():
            if isinstance(value, dict):
                parameters[key] = json.dumps(
                    value, separators=(",", ":"), ensure_ascii=False
                )

        encoded_url = urllib.parse.urlencode(parameters)
        final_url = url + "?" + encoded_url
        return final_url
