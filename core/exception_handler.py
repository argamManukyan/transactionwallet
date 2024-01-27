import logging
from typing import Iterable

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


logger = logging.getLogger()


def error_response(
    errors=dict, message="", status_code: int = status.HTTP_400_BAD_REQUEST
):
    return {
        "success": False,
        "message": message or "error",
        "data": {},
        "errors": errors,
        "status_code": status_code,
    }


def grouping_message(message: Iterable, error_key: str, errors_dict: dict) -> dict:
    """Returns formatted exceptions mapping object"""

    if isinstance(message, list) and len(message) > 1 or isinstance(message, str):
        errors_dict[error_key] = message
    elif isinstance(message, list):
        errors_dict[error_key] = message[0]

    return errors_dict


def custom_exception_handler(exc, context):
    """Call REST framework's default exception handler at first,
    to get the standard error response.
    """
    response = exception_handler(exc, context)
    logger.error("")

    # Now add the HTTP status code to the response.
    if response is not None:

        logger.error(f"error response Code: {response.status_code}, ")
        if isinstance(exc, APIException):

            try:
                response.data["params"] = exc.params

            except AttributeError:
                errors_dict = {}
                if isinstance(exc.detail, dict):
                    for error_key, message in exc.detail.items():
                        grouping_message(
                            message=message,
                            error_key=error_key,
                            errors_dict=errors_dict,
                        )
                elif isinstance(exc.detail, str):
                    grouping_message(
                        message=exc.detail,
                        error_key="detail",
                        errors_dict=errors_dict,
                    )

                if errors_dict:
                    response.data.update(errors_dict)

        response.data = error_response(
            errors={**response.data}, status_code=response.status_code
        )

    return response
