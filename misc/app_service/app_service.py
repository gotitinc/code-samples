import logging
from typing import TYPE_CHECKING

from jwt import application as application_jwttoken
from .exceptions import ApplicationServiceException


if TYPE_CHECKING:
    from aiohttp import ClientSession


class ApplicationService:
    """
    Make HTTP requests to other services with JWT signature
    """

    def __init__(
        self,
        application_key: str,
        application_secret: str,
        aiohttp_session: 'ClientSession',
    ):
        """
        Args:
            application_key (str):
            application_secret (str):
            aiohttp_session (ClientSession):
        """
        self.application_key = application_key
        self.application_secret = application_secret
        self.aiohttp_session = aiohttp_session

    async def make_request(
        self,
        request_method,
        url,
        params=None,
        payload=None,
        timeout=None,
        on_success=None,
        on_failure=None,
        response_schema=None,
        headers=None,
    ):
        """
        Make a HTTP request to a given service URL
        Args:
            request_method (str): The method of request
            url (str): The service URL
            params (dict): Parameters to be sent in the query string
            payload (dict): Data to be sent in the request body
            timeout (int, optional): The request timeout
            on_success (function, optional): A callback function when the request succeeds
            on_failure (function, optional): A callback function when the request fails
            response_schema (Marshmallow, optional): A Marshmallow schema instance
            headers (optional): Request headers
        Returns:
            dict: The request response data
        Raises:
            app_service.exception.ApplicationServiceException if the request fails
        """
        if not headers:
            authorization_token = application_jwttoken.encode(
                self.application_key, self.application_secret
            )
            headers = {'Authorization': 'Bearer {}'.format(authorization_token)}

        response_body = None
        try:
            response = await self.aiohttp_session.request(
                request_method,
                url,
                params=params,
                json=payload,
                headers=headers,
                timeout=timeout,
            )

            response_content_type = response.headers.get('Content-Type')
            if (response_content_type is not None) and (
                'application/json' in response_content_type
            ):
                response_body = await response.json()

            # Handle failure case
            if response.status >= 400:
                ApplicationService.raise_exception_from_status(
                    response.status,
                    'Error occurred when requesting to application service',
                    {'url': url, 'payload': payload, 'response': response_body},
                )
            # Validate the response if a schema was provided
            if response_schema is not None:
                response_schema.load(response_body)

            # Handle success case
            if on_success is not None:
                on_success(payload, response_body)

            return response_body
        except Exception as exception:
            if on_failure is not None:
                on_failure(payload, response_body)

            logging.exception(exception)
            raise exception

    @staticmethod
    def raise_exception_from_status(status_code, error_message, error_data):
        raise ApplicationServiceException(error_message, error_data)