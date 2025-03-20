# (C) Copyright 2019-2025 Hewlett Packard Enterprise Development LP.
# Apache License 2.0

import json
import requests
import urllib.parse, urllib3
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout


urllib3.disable_warnings()


class HPEUXIApiLogin:
    def __init__(
        self,
        url="https://api.capenetworks.com",
        api_token="",
        client_id="",
        client_secret="",
        api_client_credentials="",
        oauth_token_url="https://sso.common.cloud.hpe.com/as/token.oauth2",
        verify_ssl=True,
    ):
        """
        This is the class constructor for HPE Aruba Networking User Experience Insight API Class.

        This constructor is required to be created before any modules can be used and must contain the following function arguments:

        Mandatory Parameters Method 1:
        api_token (string): API Token for API Service

        Mandatory Parameters Method 2:
        client_id (string): oAuth API Client ID
        client_secret (string): oAuth API Client Secret

        Mandatory Parameters Method 3:
        api_client_credentials (object): dictionary object containing both 'client_id' and 'client_secret', used with Utils_UXI.get_personal_api_client_creds_from_file()

        Optional Parameters:
        url (string): Web Service for API Services  - https://api-dev.capenetworks.com
        verify_ssl (boolean): Validate web service cerificate - True/False
        oauth_token_url (string): URL for retrieving API Keys directly from GreenLake

        """
        self.url = url
        self.api_token = api_token
        self.verify_ssl = verify_ssl
        self.oauth_token_url = oauth_token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_client_credentials = api_client_credentials

    def _send_request(self, url, method, query=""):
        """Sends a request to the HPE Aruba Networking User Experience Insight API  URL
        :query: must contain the json request if model required
        :url: must contain the /url (e.g. /groups)
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
            header = {"Authorization": "Bearer " + self.api_token}
            try:
                if method == "post":
                    response = requests.post(
                        url=full_url_path,
                        json=query,
                        headers=header,
                        verify=self.verify_ssl,
                    )
                if method == "patch":
                    header["Content-Type"] = "application/merge-patch+json"
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
                    all_items = []
                    next_page = None
                    status_code = None
                    headers = None

                    while True:
                        response = requests.get(
                            url=full_url_path,
                            headers=header,
                            verify=self.verify_ssl,
                            params={"next": next_page} if next_page else None,
                        )  # added

                        response_data = response.json()
                        all_items.extend(response_data.get("items", []))
                        status_code = response.status_code
                        headers = response.headers
                        next_page = response_data.get("next")
                        if not next_page:
                            break
                    combined_response = {
                        "status_code": status_code,
                        "headers": dict(headers),
                        "data": {
                            "items": all_items,
                            "count": len(all_items),
                            "next": None,
                        },
                    }
                    response = combined_response

                if method == "delete":
                    response = requests.delete(
                        url=full_url_path,
                        json=query,
                        headers=header,
                        verify=self.verify_ssl,
                    )
                if method == "":
                    print(
                        "Method needs to be supplied before sending a request to the HPE Aruba Networking User Experience Insight API Service."
                    )
                try:
                    if method == "get":
                        if response["status_code"] == 200:
                            return response["data"]
                        else:
                            return response
                    else:
                        if response.status_code == 200:
                            return json.loads(response.text)
                        else:
                            return json.loads(response.text)
                except json.decoder.JSONDecodeError:
                    return response.text

            except Exception as err:
                print(f"An error occurred: {err}")
                return {"error": str(err)}
        else:
            print(
                "Problem logging into HPE Aruba Networking User Experience Insight API Service"
            )
            return cred


def _new_api_token(self):
    """
    Operation: Obtain an OAuth2 access token for making API calls
    Required Body Parameters: grant_type (string) = ['client_credentials']:
    Required Body Parameters: client_id (string): Client ID
    Required Body Parameters: client_secret (string): Client secret

    Required Body Parameters (type(dict) body example)- {
    "grant_type": "client_credentials",
    "client_id": "string",
    "client_secret": "string"
    }
    """

    if self.api_client_credentials == "":
        
        client_creds = HTTPBasicAuth(self.client_id, self.client_secret)
    else:
        client_creds = HTTPBasicAuth(self.api_client_credentials['client_id'], self.api_client_credentials['client_secret'])
    
    response = requests.post(
        url=self.oauth_token_url,
        data={"grant_type": "client_credentials"},
        auth=client_creds,
        verify=self.verify_ssl,
    )
    try:

        if response.status_code == 200:
            response = json.loads(str(response.text))
            return response
        else:
            response = json.loads(str(response.text))
            return (
                "Error using access_token. Is it expired, or does it exist? Please investigate. Error Details: ",
                response,
            )
        
        

    except json.decoder.JSONDecodeError:
        return response


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
