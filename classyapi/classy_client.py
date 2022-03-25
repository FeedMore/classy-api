import requests
from urllib.parse import urljoin

from datetime import datetime, timedelta


class ClassyAPIException(Exception):
    pass


class ClassyAPIClient:
    BASE_URL = "https://api.classy.org/"
    BASE_TOKEN_URL = "https://api.classy.org/oauth2/auth"
    TOKEN = None
    TOKEN_EXPIRATION = None

    def __init__(self, org_id, client_id, client_secret):
        """
        A basic client for the Classy API v2.0.  This is a basic REST API
        client using OAuth2 token authentication.

        Much of these are basic Python API calls.  Much of this is based
        off of the older classy-api-client library by dnussbaum. The main
        difference is the Token is managemenet to allow for multiple
        clients and handling of expirations.

        API Documentation: https://developers.classy.org/api-docs/v2/index.html

        :param org_id: string of organization ID
        :param client_id: string of client secret
        :param client_secret:
        """
        self.__organization_id = org_id
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__token = None
        self.__token_expiration = None
        self.__session = requests.Session()

    def __is_token_valid(self):
        """
        Checks if an access token is set or if it has expired.
        :return: boolean
        """
        return self.__token and self.__token_expiration > datetime.utcnow()

    def __set_auth_token(self):
        """
        Gets a Classy API OAuth token if the current token is empty,
        invalid, or expired.

        Response example: {'token_type': 'bearer',
        'access_token': 'Zx0x3Nh4PiVnERUQi0QCNIcvpQEApkGX',
        'expires_in': 43200}

        :return: string of the API token.
        """
        if self.__is_token_valid():
            print(self.__token, self.__token_expiration)
            return self.__token

        token_response = requests.post(
            ClassyAPIClient.BASE_TOKEN_URL,
            params={
                "grant_type": "client_credentials",
                "client_id": self.__client_id,
                "client_secret": self.__client_secret
            }
        ).json()

        if "error" in token_response:
            raise ClassyAPIException('{error}: {error_description}'.format(**token_response))

        try:
            self.__token = token_response["access_token"]
            expires = datetime.utcnow() + timedelta(seconds=token_response["expires_in"])
            self.__token_expiration = expires
        except KeyError:
            raise ClassyAPIException('Access token and token expiration not returned')

    def __api_call(self, method, endpoint, params=[], data={}):
        """
        General request method.

        :param method: string of the REST method type
        :param endpoint: string of the URL for the request.
        :param params: list of querystring arguments
        :param data: dict to send in the body of the request
        :return: json of response
        """
        if not self.__is_token_valid():
            self.__set_auth_token()

        headers = {
            "Authorization": "Bearer {}".format(self.__token)
        }
        call_url = urljoin(ClassyAPIClient.BASE_URL, endpoint)

        response = self.__session.request(
            method, call_url, params=params, json=data, headers=headers
        )

        if response.status_code == 404:
            raise ClassyAPIException("404 return for {}".format(call_url))

        if response.status_code is not requests.codes.ok:
            raise ClassyAPIException("Server responded with {}".format(response.status_code))

        return response

    def get(self, endpoint, params={}, expand=[]):

        if expand:
            params.update({"with": ",".join(expand)})

        return self.__api_call("GET", endpoint, params=params)

    def test(self):
        self.__set_auth_token()
