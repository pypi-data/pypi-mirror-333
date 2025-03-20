import os
import functools
from uplink import returns, json


def get_key():

    try:
        key = os.environ["OCP_APIM_SUBSCRIPTION_KEY"]
    except KeyError as e:
        print(
            f"""ERROR: Define the environment variable {e} with your subscription key.  For example:

        export OCP_APIM_SUBSCRIPTION_KEY="INSERT_YOUR_SUBSCRIPTION_KEY"

        """
        )
        key = None
    return key


key = get_key()


def returns_json(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return returns.json(func)(*args, **kwargs)
    return wrapper


def json_request(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return json(func)(*args, **kwargs)
    return wrapper
