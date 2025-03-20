from .module_imports import key, returns_json, json_request
from uplink.retry.when import status_5xx
from uplink import (
    Consumer,
    get as http_get,
    patch,
    headers,
    retry,
    Body,
    Query,
)


@headers({"Ocp-Apim-Subscription-Key": key})
@retry(max_attempts=20, when=status_5xx())
class Portal_Users(Consumer):
    """Inteface to portal users resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    @returns_json
    @http_get("portal-users")
    def list(
        self,
        user_uid: Query = None,
        user_role: Query = None,
        company_uid: Query = None,
    ):
        """This call will return portal user information for the specified criteria."""

    @returns_json
    @json_request
    @patch("portal-users")
    def update(self, portal_user: Body):
        """This call will update the portal user information with the specified criteria."""
