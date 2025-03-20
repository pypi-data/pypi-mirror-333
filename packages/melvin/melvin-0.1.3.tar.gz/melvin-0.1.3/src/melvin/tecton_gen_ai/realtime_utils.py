import functools

import botocore
import botocore.session
import aws_secretsmanager_caching


@functools.lru_cache()
def get_secretsmanager_cache():
    """
    Creates and returns a cached SecretCache instance for AWS Secrets Manager.
    """
    session = botocore.session.get_session()
    secretsmanager_client = session.create_client("secretsmanager")
    cache_config = aws_secretsmanager_caching.SecretCacheConfig()
    return aws_secretsmanager_caching.SecretCache(
        config=cache_config, client=secretsmanager_client
    )


def retrieve_secret_value(secret_name: str) -> str:
    """
    Retrieves a secret value from AWS Secrets Manager by its name.

    This function is optimized for multiple calls within an on-demand feature view,
    avoiding repeated AWS Secrets Manager API calls for the same secret.

    Args:
        secret_name (str): The name of the secret to retrieve.

    Returns:
        str: The secret value as a string.
    """
    cache = get_secretsmanager_cache()
    return cache.get_secret_string(secret_name)


def get_tecton_secret(scope: str, key: str) -> str:
    """
    Retrieves a secret value from the Tecton-specific Secrets Manager scope.
    This is not for users to use directly, but for Tecton to use internally.

    Args:
        scope (str): The scope of the secret.
        key (str): The key of the secret.

    Returns:
        str: The secret value as a string.
    """
    return retrieve_secret_value(f"tecton-secrets-manager/{scope}/{key}")


@functools.lru_cache()
def create_cached_client(client_class, *args, **kwargs):
    """
    Creates and caches a client instance of the specified class with given arguments.

    This function is optimized for reuse across multiple calls of an on-demand feature view,
    ensuring the same client instance is used when possible.

    Args:
        client_class: The class of the client to instantiate.
        *args: Positional arguments for client instantiation.
        **kwargs: Keyword arguments for client instantiation.

    Returns:
        An instance of the specified client class.
    """
    return client_class(*args, **kwargs)
