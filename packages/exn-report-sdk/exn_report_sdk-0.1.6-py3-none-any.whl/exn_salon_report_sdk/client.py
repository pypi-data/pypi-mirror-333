import json
from urllib.parse import parse_qs, urlencode
import requests
import urllib
from .config import BASE_URL, TIMEOUT
from .exceptions import AuthenticationError, RequestError
from .utils import (
    format_date_range_offset,
    format_from_date_to_date_by_offset,
    format_query_params_to_query_string,
    generate_headers,
    get_string_to_sign,
    get_timestamp,
    modify_query_string,
    serialize_payload,
)
import hmac
import hashlib
import base64
from datetime import datetime


class ReportClient:
    def __init__(
        self,
        api_key: str,
        secret_key: str,
        ref_id: int,
        base_url: str = BASE_URL,
        offset: int = 7,
    ):
        """
        Initializes the API client with authentication and configuration settings.

        Args:
            api_key (str): The API key used for authentication.
            secret_key (str): The secret key used for generating request signatures.
            base_url (str, optional): The base URL of the API. Defaults to BASE_URL.
            ref_id (int): A reference ID used for specific API requests.
            offset (int, optional): The time offset (in hours) for timestamp calculations. Defaults to 7.
        """
        self.api_key = api_key  # Store API key for authentication
        self.secret_key = secret_key  # Store secret key for HMAC signature
        self.base_url = base_url  # Store base URL for API requests
        self.ref_id = ref_id  # Store reference ID for API operations (if applicable)
        self.offset = offset  # Store time offset (default is 7 hours)

    def get_report(self, end_point: str, body: dict = None, params: dict = None):
        """
        Sends a GET request to retrieve a report from the API.

        Args:
            end_point (str): The API endpoint for fetching the report.
            body (dict, optional): The request payload containing report details. Defaults to None.

        Returns:
            dict: The JSON response from the API.

        Raises:
            AuthenticationError: If the API key or signature is invalid (HTTP 401).
            RequestError: If the request fails or encounters an HTTP error.
        """
        query_string = format_query_params_to_query_string(params, self.ref_id)
        query_string = modify_query_string(query_string, self.offset)
        url = f"{self.base_url}{end_point}?{query_string}"  # Construct full URL
        headers = generate_headers(
            self.api_key, self.secret_key, method="GET", end_point=end_point, body=body
        )  # Generate headers

        try:
            response = requests.get(
                url, headers=headers, timeout=TIMEOUT
            )  # Send GET request
            response.raise_for_status()  # Raise error for HTTP failures
            return response  # Return parsed JSON response
        except requests.exceptions.HTTPError as e:
            if response.status_code == 500:
                raise RequestError(
                    f"HTTP error: {response.status_code}: {str(e)}"
                ) from e
            return response
        except requests.exceptions.RequestException as e:
            raise RequestError(
                "Request failed."
            ) from e  # Handle general request exceptions

    def create_report(self, end_point: str, body: dict = None, params: dict = None):
        """
        Sends a POST request to create a new report.

        Args:
            end_point (str): The API endpoint for creating the report.
            body (dict, optional): The request payload containing report details. Defaults to None.

        Returns:
            dict: The JSON response from the API.

        Raises:
            AuthenticationError: If the API key or signature is invalid (HTTP 401).
            RequestError: If the request fails or encounters an HTTP error.
        """
        query_string = format_query_params_to_query_string(params, self.ref_id)
        query_string = modify_query_string(query_string, self.offset)
        url = f"{self.base_url}{end_point}?{query_string}"  # Construct full URL
        # payload = json.dumps(body)  # Convert body to JSON string
        headers = generate_headers(
            self.api_key, self.secret_key, method="POST", end_point=end_point, body=body
        )  # Generate headers

        try:
            response = requests.post(
                url, headers=headers, json=body, timeout=TIMEOUT
            )  # Send POST request
            response.raise_for_status()  # Raise error for HTTP failures
            return response  # Return parsed JSON response
        except requests.exceptions.HTTPError as e:
            if response.status_code == 500:
                raise RequestError(
                    f"HTTP error: {response.status_code}: {str(e)}"
                ) from e
            return response
        except requests.exceptions.RequestException as e:
            raise RequestError(
                "Request failed."
            ) from e  # Handle general request exceptions

    def get_list_report(self, body: dict = None, params: dict = {}):
        """
        Endpoint: /api/report/
        Required params: from_date, to_date, report_type
        - from_date: YYYY-MM-dd / YYYY-MM-dd HH:mm:ss
        - to_date: YYYY-MM-dd / YYYY-MM-dd HH:mm:ss
        - report_type: SALE, SALE_SERVICE, SALE_ADD_ON, DEDUCTION, DISCOUNT, SOLD_GIFT_CARD
        """
        end_point = "/api/report/"
        return self.get_report(end_point=end_point, body=body, params=params)

    def get_total_report(self, body: dict = None, params: dict = {}):
        """
        Endpoint: /api/report/total/
        Required params: from_date, to_date, report_type
        - from_date: YYYY-MM-dd / YYYY-MM-dd HH:mm:ss
        - to_date: YYYY-MM-dd / YYYY-MM-dd HH:mm:ss
        - report_type: SALE, SALE_SERVICE, SALE_ADD_ON, DEDUCTION, DISCOUNT, SOLD_GIFT_CARD, TIP
        """
        end_point = "/api/report/total/"
        return self.get_report(end_point=end_point, body=body, params=params)

    def get_summary_report(self, body: dict = None, params: dict = {}):
        """
        Endpoint: /api/report/summary/
        Required params: from_date, to_date
        - from_date: YYYY-MM-dd / YYYY-MM-dd HH:mm:ss
        - to_date: YYYY-MM-dd / YYYY-MM-dd HH:mm:ss
        """
        end_point = "/api/report/summary/"
        return self.get_report(end_point=end_point, body=body, params=params)

    def push_data_report(self, body: dict, params: dict = {}):
        """
        Endpoint: /api/report/add-data/
        """
        params["source_id"] = body.get("id")
        end_point = "/api/report/add-data/"
        return self.create_report(
            end_point=end_point, body=serialize_payload(body), params=params
        )
