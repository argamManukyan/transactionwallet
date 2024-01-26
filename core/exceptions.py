from rest_framework import status
from rest_framework.exceptions import APIException


class NotEnoughFunds(APIException):

    default_detail = "Not enough funds, please try another amount"
    status_code = status.HTTP_400_BAD_REQUEST
