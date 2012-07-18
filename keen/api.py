import requests
from keen import exceptions

__author__ = 'dkador'

class KeenApi(object):
    """
    Responsible for communicating with the Keen API. Used by multiple
    persistence strategies or async processing.
    """

    # the default base URL of the Keen API
    base_url = "https://api.keen.io"
    # the default version of the Keen API
    api_version = "2.0"

    def __init__(self, project_id, auth_token, base_url=None,
                 api_version=None):
        """ Initializes a KeenApi object

        :param project_id: the Keen project ID
        :param auth_token: the Keen authorization token
        :param base_url: optional, set this to override where API requests
        are sent
        :param api_version: string, optional, set this to override what API
        version is used
        """
        super(KeenApi, self).__init__()
        self.project_id = project_id
        self.auth_token = auth_token
        if base_url:
            self.base_url = base_url
        if api_version:
            self.api_version = api_version

    def post_event(self, event):
        """ Posts a single event to the Keen API.

        :param event: an Event to upload
        """
        url = "{}/{}/projects/{}/{}".format(self.base_url, self.api_version,
                                            self.project_id,
                                            event.collection_name)
        headers = {"Authorization": self.auth_token,
                   "Content-Type": "application/json"}
        payload = event.to_json()
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code != 201:
            error = response.json
            raise exceptions.KeenApiError(error)