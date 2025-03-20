from .module_imports import key, returns_json, json_request
from uplink.retry.when import status_5xx
from uplink import (
    Consumer,
    get as http_get,
    post,
    patch,
    delete,
    headers,
    retry,
    Body,
    Query,
)


@headers({"Ocp-Apim-Subscription-Key": key})
@retry(max_attempts=20, when=status_5xx())
class Oracle_Users(Consumer):
    """Inteface to Oracle users resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    @returns_json
    @http_get("oracle-users")
    def list(
        self,
        email: Query = None,
        userName: Query = None,
    ):
        """This call will return Oracle user information for the specified criteria."""

    @returns_json
    @http_get("oracle-users/{email}")
    def get(
        self,
        email: str,
    ):
        """This call will return the Oracle user for the specified email."""

    @returns_json
    @json_request
    @post("oracle-users")
    def insert(
        self,
        oracle_user: Body,
    ):
        """This call will insert a new Oracle user."""

    @returns_json
    @json_request
    @patch("oracle-users/batch")
    def batch_update(
        self,
        oracle_user_batch: Body,
    ):
        """This call will update a batch of Oracle users."""

    @returns_json
    @json_request
    @patch("oracle-users/{email}")
    def update(
        self,
        email: str,
        oracle_user: Body,
    ):
        """This call will update a Oracle user."""

    @json_request
    @delete("oracle-users/{email}")
    def delete(
        self,
        email: str,
    ):
        """This call will delete a Oracle user."""
