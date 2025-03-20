from typing import Dict, Optional

import httpx


class HttpClient:
    """
    Base HTTP Client class to make requests to a given base URL. This class is meant to be inherited by other classes
    that will implement the actual API clients.

    This class uses the HTTPX library to make requests. It provides methods to make GET, POST, PUT, PATCH, and DELETE,
    it will return the httpx Response object, that will contain the following values.

    - status_code: The status code of the response.
    - reason_phrase: The reason phrase of the response.
    - http_version: The HTTP version of the response.
    - headers: The headers of the response.
    - text: The response body as a string.
    - json: The response body as a JSON object.
    - content: The response body as bytes.
    - request: The request object that was sent.
    - url: The URL of the response.
    - history: The history of the response

    """

    def __init__(self, url: str, **kwargs) -> None:
        """
        Initialize the HTTP Client with the base URL, headers, and timeout.

        :param url:
        The Proxy URL to use for requests. This can be a URL with or without the protocol.
        If the protocol is not provided, HTTPS is assumed.

        Keyword Arguments
        - headers: A dictionary of headers to include in the request. Defaults to JSON responses
        - timeout: The timeout for the request in seconds.
        - allow_http_access: A boolean to allow HTTP access. If set to False, only HTTPS URLs are allowed.

        """
        self._base_url = url.rstrip("/")
        self.client = None
        self._cookie_domain = None
        self._last_response = None
        self._timeout = kwargs.get("timeout", 10)
        self._allow_http_access = kwargs.get("allow_http_access", False)
        self._headers = kwargs.get(
            "headers",
            {"accept": "application/json", "content-type": "application/json"},
        )

        if not url.startswith("http://") and not url.startswith("https://"):
            self._base_url = f"https://{url}"
        if not self.allow_http_access and not self.base_url.startswith("https://"):
            self.client = None
            raise ValueError("Only HTTPS URLs are allowed.")

        self._base_url = self._base_url.rstrip("/")
        self.client = httpx.Client(
            base_url=self._base_url,
            headers=httpx.Headers(self._headers),
            timeout=self._timeout,
            follow_redirects=True,
        )

    @property
    def base_url(self) -> str:
        """The base URL for the client."""
        return self._base_url

    @base_url.setter
    def base_url(self, url: str) -> None:
        """Set the base URL for the client."""
        url = url.rstrip("/")
        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"https://{url}"
        if not self.allow_http_access and not url.startswith("https://"):
            raise ValueError("Only HTTPS URLs are allowed.")
        self._base_url = url
        self.client = httpx.Client(
            base_url=self._base_url,
            headers=httpx.Headers(self._headers),
            timeout=self._timeout,
            follow_redirects=True,
        )

    @property
    def timeout(self) -> int:
        """The timeout for the client."""
        return self._timeout

    @timeout.setter
    def timeout(self, timeout: int) -> None:
        """Set the timeout for the client. (in seconds)"""
        self._timeout = timeout
        self.client.timeout = timeout

    @property
    def allow_http_access(self) -> bool:
        """A boolean to allow HTTP access."""
        return self._allow_http_access

    @allow_http_access.setter
    def allow_http_access(self, allow: bool) -> None:
        """Set the allow_http_access property. If set to False, only HTTPS URLs are allowed."""
        self._allow_http_access = allow

    @property
    def headers(self) -> Dict:
        """The headers for the client."""
        return dict(self._headers)

    @headers.setter
    def headers(self, headers: Dict) -> None:
        """Set the headers for the client."""
        self._headers = httpx.Headers(headers)

    @property
    def cookie_domain(self) -> str | None:
        """The domain to set cookies for."""
        return self._cookie_domain

    @cookie_domain.setter
    def cookie_domain(self, domain: str | None) -> None:
        """Set the domain to set cookies for."""
        self._cookie_domain = domain

    def set_cookie(self, key: str, value: str, domain: str = None) -> None:
        """Set a cookie for the client."""
        if domain is None:
            self.client.cookies.set(key, value)
        else:
            self.client.cookies.set(key, value, domain=domain)

    def get_cookies(self) -> Dict:
        """Get the cookies from the client."""
        return dict(self.client.cookies)

    def get_cookie_jar(self) -> httpx.Cookies:
        """Get the cookies from the client."""
        return self.client.cookies

    def clear_cookies(self) -> None:
        """Clear all cookies from the client."""
        self.client.cookies.clear()

    def get(self, endpoint: str, params: Optional[Dict] = None) -> httpx.Response:
        """
        Make a GET request to the given endpoint with the given parameters.

        :param endpoint:
        The api endpoint to make the request to. do not include the base URL, just the endpoint.
        :param params:
        The parameters to include in the request. this should be a dictionary of key-value pairs., it is
        optional

        :return: The response object from the request. it is an httpx.Response object.
        """
        my_endpoint = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.client.get(my_endpoint, params=params, timeout=self.timeout, headers=self.headers)
        return response

    def post(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> httpx.Response:
        """
        Make a POST request to the given endpoint with the given data.

        :param endpoint: The api endpoint to make the request to. do not include the base URL, just the endpoint.
        :param data: The data to include in the request. Use this for form data. Optional
        :param json: The JSON data to include in the request. Use this for JSON data. Optional
        :return: The response object from the request. it is an httpx.Response object.
        """
        my_endpoint = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.client.post(
            my_endpoint,
            data=data,
            json=json,
            timeout=self.timeout,
            headers=self.headers,
        )

    def put(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> httpx.Response:
        """
        Make a PUT request to the given endpoint with the given data. (This is a Full Object update)

        :param endpoint: The api endpoint to make the request to. do not include the base URL, just the endpoint.
        :param data: The data to include in the request. Use this for form data. Optional
        :param json: The JSON data to include in the request. Use this for JSON data. Optional
        :return: The response object from the request. it is an httpx.Response object.
        """
        my_endpoint = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.client.put(
            my_endpoint,
            data=data,
            json=json,
            timeout=self.timeout,
            headers=self.headers,
        )

    def patch(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> httpx.Response:
        """
        Make a PUT request to the given endpoint with the given data. (This is a change onnly update)

        :param endpoint: The api endpoint to make the request to. do not include the base URL, just the endpoint.
        :param data: The data to include in the request. Use this for form data. Optional
        :param json: The JSON data to include in the request. Use this for JSON data. Optional
        :return: The response object from the request. it is an httpx.Response object.
        """
        my_endpoint = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.client.patch(
            my_endpoint,
            data=data,
            json=json,
            timeout=self.timeout,
            headers=self.headers,
        )

    def delete(self, endpoint: str) -> httpx.Response:
        """
        Make a DELETE request to the given endpoint.

        :return: The response object from the request. it is an httpx.Response object.
        """
        my_endpoint = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.client.delete(my_endpoint, timeout=self.timeout, headers=self.headers)

    def close(self):
        self.client.close()
