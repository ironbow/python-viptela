"""Cisco vManage Event API Methods.
"""

from vmanage.api.http_methods import HttpMethods
from vmanage.data.parse_methods import ParseMethods
from vmanage.utils import list_to_dict


class Event(object):
    """vManage Event  API

    Responsible for DELETE, GET, POST, PUT methods against vManage
    Event.

    """

    def __init__(self, session, host, port=443):
        """Initialize Event object with session parameters.

        Args:
            session (obj): Requests Session object
            host (str): hostname or IP address of vManage
            port (int): default HTTPS 443

        """

        self.session = session
        self.host = host
        self.port = port
        self.base_url = f"https://{self.host}:{self.port}/dataservice/"

    def get_event_list(self, time_range=1):
        """Obtain a list of specified device type

        Args:
            time_range (str): range of time to get events for (in hours)

        Returns:
            result (dict): All data associated with a response.
        """

        url = f"{self.base_url}event"
        payload = {
            "query": {
                "condition": "AND",
                "rules": [
                    {
                        "value": [str(time_range)],
                        "field": "entry_time",
                        "type": "date",
                        "operator": "last_n_hours",
                    }
                ],
            },
            "size": 10000,
        }
        response = HttpMethods(self.session, url).request("GET", payload=payload)
        result = ParseMethods.parse_data(response)
        return result
