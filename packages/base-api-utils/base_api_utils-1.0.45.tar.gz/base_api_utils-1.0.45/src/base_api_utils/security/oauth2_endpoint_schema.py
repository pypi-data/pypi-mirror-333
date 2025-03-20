from ..utils import config
from drf_spectacular.utils import extend_schema


def extend_oauth2_schema(path, method, **extend_kwargs):
    """
    Decorator to expand @extend_schema documentation based on settings.OAUTH2.CLIENT.ENDPOINTS
    """
    def decorator(func):
        endpoints = config('OAUTH2.CLIENT.ENDPOINTS')
        endpoint = endpoints.get(path, {}).get(method.lower(), None) if endpoints else {}

        description = extend_kwargs.get('description', None)
        scopes = ''

        if endpoint:
            description = description if description else endpoint.get('desc', '')
            scopes = endpoint.get('scopes', '')
            if scopes:
                description = f'{description} - Scopes: {scopes}'

        return extend_schema(
            description=description,
            extensions={'x-scopes': scopes.split()},
            **extend_kwargs
        )(func)

    return decorator
