from unittest.mock import patch, MagicMock

# Import the functions we want to test
from src.tecton_gen_ai.realtime_utils import (
    get_secretsmanager_cache,
    retrieve_secret_value,
    create_cached_client,
    get_tecton_secret,
)


@patch("botocore.session.get_session")
@patch("aws_secretsmanager_caching.SecretCache")
def test_get_secretsmanager_cache(MockSecretCache, mock_get_session):
    # Arrange
    mock_client = MagicMock()
    mock_get_session.return_value = mock_client
    mock_cache_instance = MagicMock()
    MockSecretCache.return_value = mock_cache_instance

    # Act
    result = get_secretsmanager_cache()

    print(result)

    # Assert
    mock_client.create_client.assert_called_once_with("secretsmanager")
    MockSecretCache.assert_called_once()
    assert result == mock_cache_instance


@patch("src.tecton_gen_ai.realtime_utils.get_secretsmanager_cache")
def test_retrieve_secret_value(mock_get_cache):
    # Arrange
    mock_cache = MagicMock()
    mock_cache.get_secret_string.return_value = "test_secret_value"
    mock_get_cache.return_value = mock_cache

    # Act
    result = retrieve_secret_value("test_secret_name")

    # Assert
    assert result == "test_secret_value"
    mock_cache.get_secret_string.assert_called_once_with("test_secret_name")


@patch("src.tecton_gen_ai.realtime_utils.get_secretsmanager_cache")
def test_get_tecton_secret(mock_get_cache):
    # Arrange
    mock_cache = MagicMock()
    mock_cache.get_secret_string.return_value = "test_secret_value"
    mock_get_cache.return_value = mock_cache

    # Act
    result = get_tecton_secret(scope="tecton-realtime", key="test_secret_name")

    # Assert
    assert result == "test_secret_value"
    mock_cache.get_secret_string.assert_called_once_with(
        "tecton-secrets-manager/tecton-realtime/test_secret_name"
    )


def test_create_cached_client():
    # Arrange
    class TestClient:
        def __init__(self, arg1, arg2, kwarg1=None):
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg1 = kwarg1

    # Act
    client1 = create_cached_client(TestClient, "arg1", "arg2", kwarg1="test")
    client2 = create_cached_client(TestClient, "arg1", "arg2", kwarg1="test")
    client3 = create_cached_client(TestClient, "different_arg", "arg2")

    # Assert
    assert client1 is client2
    assert client1 is not client3
    assert client1.arg1 == "arg1"
    assert client1.arg2 == "arg2"
    assert client1.kwarg1 == "test"
    assert client3.arg1 == "different_arg"
