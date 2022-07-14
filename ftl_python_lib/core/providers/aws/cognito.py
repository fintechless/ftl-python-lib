"""
Provider for AWS Cognito
"""

import base64
import hashlib
import hmac
import random
import string

import boto3
import requests

from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.decorators.exponential_backoff import DecoratorExponentialBackoff


# pylint: disable=R0903
class ProviderCognito:
    """
    Provider for AWS Cognito
    """

    def __init__(
        self,
        request_context: RequestContext,
        environ_context: EnvironmentContext,
    ) -> None:
        """
        Constructor
        """

        LOGGER.logger.debug("Creating Cognito provider")

        self.__request_context = request_context
        self.__environ_context = environ_context

    @DecoratorExponentialBackoff.retry(Exception)
    def get_access_token(
        self,
        grant_type: str = "client_credentials",
        scope: str = "api/public.read",
        content_type: str = "application/x-www-form-urlencoded",
    ) -> str:
        """
        Get Cognito access token
        :param grant_type: The Cognito User Pool grant type
        :type grant_type: str
        :param scope: The Cognito User Pool scope
        :type scope: str
        :param content_type: The Content-type
        :type content_type: str
        """

        body = {"grant_type": grant_type, "scope": scope}

        headers = {"Content-Type": content_type}
        auth_url: str = (
            "https://auth." + self.__environ_context.api_domain + "/oauth2/token"
        )

        response = requests.post(
            url=auth_url,
            data=body,
            auth=(
                self.__environ_context.aws_cognito_client_id,
                self.__environ_context.aws_cognito_client_secret,
            ),
            headers=headers,
        )

        return response.json()["access_token"]

    @DecoratorExponentialBackoff.retry(Exception)
    def get_secret_hash(self, username):
        msg = username + self.__environ_context.aws_cognito_client_id
        dig = hmac.new(
            str(
                self.__environ_context.aws_cognito_client_secret,
            ).encode("utf-8"),
            msg=str(msg).encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()
        d2 = base64.b64encode(dig).decode()
        return d2

    @DecoratorExponentialBackoff.retry(Exception)
    def invite(self, email: str):
        client = boto3.client(
            "cognito-idp", region_name=self.__environ_context.active_region
        )
        try:
            response = client.admin_create_user(
                UserPoolId=self.__environ_context.aws_cognito_user_pool_id,
                Username=email,
                UserAttributes=[{"Name": "email", "Value": email}],
                ValidationData=[{"Name": "email", "Value": email}],
                TemporaryPassword=self.randomStringwithDigitsAndSymbols(10),
                ForceAliasCreation=True,
                DesiredDeliveryMediums=[
                    "EMAIL",
                ],
            )

            return {
                "status": "OK",
                "message": "Please confirm your signup, check Email for validation code",
                "code": 201,
                "data": response,
            }
        except client.exceptions.UsernameExistsException as e:
            return {
                "status": "Conflict",
                "message": "This username already exists",
                "code": 409,
                "data": {},
            }
        except client.exceptions.InvalidPasswordException as e:
            return {
                "status": "Not Acceptable",
                "message": "Password should have Caps, Special chars, Numbers",
                "code": 406,
                "data": {},
            }
        except client.exceptions.UserLambdaValidationException as e:
            return {
                "status": "Conflict",
                "message": "Email already exists",
                "code": 409,
                "data": {},
            }

    def randomStringwithDigitsAndSymbols(self, stringLength=10):
        random_source = string.ascii_letters + string.digits + string.punctuation
        # select 1 lowercase
        password = random.choice(string.ascii_lowercase)
        # select 1 uppercase
        password += random.choice(string.ascii_uppercase)
        # select 1 digit
        password += random.choice(string.digits)
        # select 1 special symbol
        password += random.choice(string.punctuation)

        # generate other characters
        for i in range(stringLength):
            password += random.choice(random_source)

        password_list = list(password)
        # shuffle all characters
        random.SystemRandom().shuffle(password_list)
        password = "".join(password_list)
        return password
