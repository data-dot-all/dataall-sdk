import os
from unittest.mock import patch

from dataall_core.base_client import BaseClient
from dataall_core.dataall_client import DataallClient
from dataall_core.profile import get_profile

import dataall_sdk

PROFILE_CONFIG = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "profile_config", "config.yaml"
)


def test_default_client_init():
    client = dataall_sdk.client()
    assert client
    assert isinstance(client, BaseClient)
    assert client.authorizer.profile is None


def test_default_client_init_with_headers():
    client = dataall_sdk.client(custom_headers={"x": "y"})
    assert client
    assert isinstance(client, BaseClient)
    assert client.custom_headers == {"x": "y"}


def test_profile1_client_init():
    client = dataall_sdk.client(profile="CognitoDefault", config_path=PROFILE_CONFIG)
    assert client
    assert isinstance(client, BaseClient)
    assert client.authorizer.profile

    config = get_profile("CognitoDefault", config_path=PROFILE_CONFIG)
    assert client.authorizer.profile == config


def test_profile2_client_init():
    client = dataall_sdk.client(profile="CustomDefault", config_path=PROFILE_CONFIG)
    assert client
    assert isinstance(client, BaseClient)
    assert client.authorizer.profile

    config = get_profile("CustomDefault", config_path=PROFILE_CONFIG)
    assert client.authorizer.profile == config


def test_default_client_loaded_methods():
    client = dataall_sdk.client(profile="CustomDefault", config_path=PROFILE_CONFIG)
    op_dict = DataallClient().op_dict

    # Get Added Methods
    built_ins = [
        method
        for method in dir(BaseClient)
        if callable(getattr(BaseClient, method)) and not method.startswith("__")
    ]
    added_methods = [
        method
        for method in dir(client)
        if callable(getattr(client, method)) and not method.startswith("__")
    ]
    method_list = set(added_methods) - set(built_ins)

    # For Each Assert Called With
    with patch.object(client, "execute") as mock_execute:
        for method in method_list:
            assert getattr(client, method)()
            mock_execute.assert_called_with(
                op_dict[method]["operation_name"],
                op_dict[method]["query_definition"],
                {},
            )
            assert getattr(client, method).__doc__ == op_dict[method]["docstring"]
