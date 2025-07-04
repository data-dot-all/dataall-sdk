import json
from unittest.mock import MagicMock

import boto3
import pytest
from moto import mock_aws

import dataall_sdk
from dataall_sdk.utils import (
    DA_OBJ_GET_FUNCTIONS,
    wait_glue_crawlers_are_completed,
    wait_share_requests_are_processed,
    wait_stacks_are_completed,
    wait_stacks_are_in_progress,
)

REGION = "us-east-1"


@pytest.fixture(scope="function")
def aws_glue():
    with mock_aws():
        yield boto3.client("glue", region_name=REGION)


def generate_creds(*args, **kwargs):
    return json.dumps(
        {"AccessKey": "Test", "SessionKey": "Test", "sessionToken": "Test"}
    )


@pytest.fixture(scope="function")
def create_crawler(aws_glue):
    aws_glue.create_crawler(
        Name="testcrawler",
        Role="testrole",
        DatabaseName="testdb",
        Targets={
            "S3Targets": [
                {"Path": "s3://testbucket/testpath"},
            ]
        },
    )
    yield


def test_get_functions_callable():
    client = dataall_sdk.client()
    for k, v in DA_OBJ_GET_FUNCTIONS.items():
        assert getattr(client, v[0]) and callable(getattr(client, v[0]))


@pytest.fixture
def mock_client(request):
    mock = MagicMock()
    setattr(mock, request.param[0], MagicMock(side_effect=request.param[1]))
    return mock


@pytest.fixture
def mock_time_sleep(mocker):
    mocker.patch("time.sleep", return_value=None)


@pytest.mark.parametrize(
    "mock_client",
    (
        [
            ("get_environment", [{"stack": {"status": "CREATE_IN_PROGRESS"}}]),
            ("get_environment", [{"stack": {"status": "CREATE_FAILED"}}]),
        ]
    ),
    indirect=True,
)
def test_wait_stacks_are_in_progress(mock_client, mock_time_sleep):
    clients = [mock_client]
    target_uris = ["uri1"]
    dataall_objects = ["environment"]

    response = wait_stacks_are_in_progress(clients, target_uris, dataall_objects)
    assert response
    mock_client.get_environment.assert_called_once_with(environmentUri="uri1")


@pytest.mark.parametrize(
    "mock_client",
    (
        [
            (
                "get_dataset",
                [
                    {"stack": {"status": "CREATE_IN_PROGRESS"}},
                    {"stack": {"status": ""}},
                    {"stack": {"status": "CREATE_IN_PROGRESS"}},
                    {"stack": {"status": "PENDING"}},
                ],
            )
        ]
    ),
    indirect=True,
)
def test_wait_stacks_are_in_progress_multiple(mock_client, mock_time_sleep):
    clients = [mock_client, mock_client]
    target_uris = ["uri1", "uri2"]
    dataall_objects = ["dataset", "dataset"]

    response = wait_stacks_are_in_progress(clients, target_uris, dataall_objects)
    assert response
    mock_client.get_dataset.assert_called_with(datasetUri="uri2")
    assert mock_client.get_dataset.call_count == 4


@pytest.mark.parametrize(
    "mock_client",
    ([("get_sagemaker_notebook", [{"stack": {"status": ""}}])]),
    indirect=True,
)
def test_wait_stacks_are_in_progress_timeout(mock_client):
    clients = [mock_client]
    target_uris = ["uri1"]
    dataall_objects = ["notebook"]

    with pytest.raises(TimeoutError):
        wait_stacks_are_in_progress(
            clients, target_uris, dataall_objects, timeout=0, sleep_time=1
        )
    mock_client.get_sagemaker_notebook.assert_called_once()


@pytest.mark.parametrize(
    "mock_client",
    (
        [
            ("get_sagemaker_notebook", [{"stack": {"status": "CREATE_COMPLETE"}}]),
            ("get_sagemaker_notebook", [{"stack": {"status": "CREATE_FAILED"}}]),
        ]
    ),
    indirect=True,
)
def test_wait_stacks_are_complete(mock_client, mock_time_sleep):
    clients = [mock_client]
    target_uris = ["uri1"]
    dataall_objects = ["notebook"]

    response = wait_stacks_are_completed(clients, target_uris, dataall_objects)
    assert response
    mock_client.get_sagemaker_notebook.assert_called_once_with(notebookUri="uri1")


@pytest.mark.parametrize(
    "mock_client",
    (
        [
            (
                "get_sagemaker_studio_user",
                [
                    {
                        "stack": {
                            "status": "UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS"
                        }
                    },
                    {"stack": {"status": "ROLLBACK_FAILED"}},
                    {"stack": {"status": "UPDATE_COMPLETE"}},
                    {"stack": {"status": "ROLLBACK_FAILED"}},
                ],
            )
        ]
    ),
    indirect=True,
)
def test_wait_stacks_are_complete_multiple(mock_client, mock_time_sleep):
    clients = [mock_client, mock_client]
    target_uris = ["uri1", "uri2"]
    dataall_objects = ["mlstudio_user", "mlstudio_user"]

    response = wait_stacks_are_completed(clients, target_uris, dataall_objects)
    assert response
    mock_client.get_sagemaker_studio_user.assert_called_with(
        sagemakerStudioUserUri="uri2"
    )
    assert mock_client.get_sagemaker_studio_user.call_count == 4


@pytest.mark.parametrize(
    "mock_client",
    ([("get_environment", [{"stack": {"status": "PENDING"}}])]),
    indirect=True,
)
def test_wait_stacks_are_complete_timeout(mock_client):
    clients = [mock_client]
    target_uris = ["uri1"]
    dataall_objects = ["environment"]

    with pytest.raises(TimeoutError):
        wait_stacks_are_completed(
            clients, target_uris, dataall_objects, timeout=0, sleep_time=1
        )
    mock_client.get_environment.assert_called_once()


@pytest.mark.parametrize(
    "mock_client", ([("get_share_object", [{"status": "Processed"}])]), indirect=True
)
def test_wait_share_requests_are_processed(mock_client, mock_time_sleep):
    clients = [mock_client]
    target_uris = ["uri1"]

    response = wait_share_requests_are_processed(clients, target_uris)
    assert response
    mock_client.get_share_object.assert_called_once_with(shareUri="uri1")


@pytest.mark.parametrize(
    "mock_client",
    (
        [
            (
                "get_share_object",
                [
                    {"status": "Share_Approved"},
                    {"status": "Share_In_Progress"},
                    {"status": "Processed"},
                    {"status": "Processed"},
                ],
            )
        ]
    ),
    indirect=True,
)
def test_wait_share_requests_are_processed_multiple(mock_client, mock_time_sleep):
    clients = [mock_client, mock_client]
    target_uris = ["uri1", "uri2"]

    response = wait_share_requests_are_processed(clients, target_uris)
    assert response
    mock_client.get_share_object.assert_called_with(shareUri="uri2")
    assert mock_client.get_share_object.call_count == 4


@pytest.mark.parametrize(
    "mock_client",
    ([("get_share_object", [{"stack": {"status": "PENDING"}}])]),
    indirect=True,
)
def test_wait_share_requests_are_processed_timeout(mock_client):
    clients = [mock_client]
    target_uris = ["uri1"]

    with pytest.raises(TimeoutError):
        wait_share_requests_are_processed(clients, target_uris, timeout=0, sleep_time=1)
    mock_client.get_share_object.assert_called_once()


@pytest.mark.parametrize(
    "mock_client", ([("generate_dataset_access_token", generate_creds)]), indirect=True
)
def test_wait_glue_crawlers_are_completed(
    mock_client, mock_time_sleep, create_crawler, aws_glue
):
    clients = [mock_client]
    target_uris = ["uri1"]
    regions = [REGION]
    crawler_names = ["testcrawler"]

    response = wait_glue_crawlers_are_completed(
        clients, target_uris, regions, crawler_names
    )
    assert response
    mock_client.generate_dataset_access_token.assert_called_once_with(datasetUri="uri1")


@pytest.mark.parametrize(
    "mock_client", ([("generate_dataset_access_token", generate_creds)]), indirect=True
)
def test_wait_wait_glue_crawlers_are_completed_timeout(
    mock_client, mock_time_sleep, create_crawler, aws_glue
):
    clients = [mock_client]
    target_uris = ["uri1"]
    regions = [REGION]
    crawler_names = ["testcrawler"]
    aws_glue.start_crawler(Name=crawler_names[0])
    with pytest.raises(TimeoutError):
        wait_glue_crawlers_are_completed(
            clients, target_uris, regions, crawler_names, timeout=0, sleep_time=1
        )
