import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from http import HTTPMethod
from threading import Lock
from typing import Any, Dict, List, Tuple, Union

import requests

log = logging.getLogger()


class _SupersetApiBase:
    """
    Base class for interacting with the Superset API.
    Handles authentication, token refresh, and making requests.
    """

    def __init__(self, base_url: str, username: str, password: str, provider: str):
        """
        Initialize the Superset API base class.

        :param base_url: The base URL of the Superset instance.
        :param username: The username for authentication.
        :param password: The password for authentication.
        :param provider: The authentication provider.
        """
        self.api_url = f"{base_url}/api/v1"
        self.username = username
        self.password = password
        self.provider = provider
        self.access_token = None
        self.refresh_token = None
        self.lock = Lock()
        self._authenticate()

    def _authenticate(self) -> None:
        """
        Authenticate with the Superset API and obtain access and refresh tokens.
        """
        payload = {
            "username": self.username,
            "password": self.password,
            "provider": self.provider,
            "refresh": True,
        }
        try:
            response = requests.post(f"{self.api_url}/security/login", json=payload)
            response.raise_for_status()
            tokens = response.json()
            self.access_token = tokens["access_token"]
            self.refresh_token = tokens["refresh_token"]
            log.debug("Authentication successful")
        except requests.RequestException as e:
            log.error(f"Authentication failed: {e}")
            raise

    def _refresh(self) -> None:
        """
        Refresh the access token using the refresh token.
        """
        payload = {"refresh_token": self.refresh_token}
        try:
            response = requests.post(f"{self.api_url}/security/refresh", json=payload)
            if response.status_code == 401:
                self._authenticate()
            else:
                response.raise_for_status()
                tokens = response.json()
                self.access_token = tokens["access_token"]
                self.refresh_token = tokens["refresh_token"]
                log.info("Token refresh successful")
        except requests.RequestException as e:
            log.error(f"Token refresh failed: {e}")
            raise

    def _request(
        self, method: HTTPMethod, endpoint: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Make a request to the Superset API.

        :param method: The HTTP method to use for the request.
        :param endpoint: The API endpoint to request.
        :param kwargs: Additional arguments to pass to the request.
        :return: The JSON response from the API.
        """
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.access_token}"
        try:
            response = requests.request(
                method, f"{self.api_url}{endpoint}", headers=headers, **kwargs
            )
            if response.status_code == 401:
                with self.lock:
                    self._refresh()
                    headers["Authorization"] = f"Bearer {self.access_token}"
                    response = requests.request(
                        method, f"{self.api_url}{endpoint}", headers=headers, **kwargs
                    )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            log.error(f"Request to {endpoint} failed: {e}")
            raise

    def _parallel_requests(
        self, requests_list: List[Tuple[HTTPMethod, str, Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """
        Make multiple requests to the Superset API in parallel.

        :param requests_list: A list of tuples containing the HTTP method, endpoint, and arguments for each request.
        :return: A list of JSON responses from the API.
        """
        results = []
        with ThreadPoolExecutor() as executor:
            future_to_request = {
                executor.submit(self.request, *request): request
                for request in requests_list
            }
            for future in as_completed(future_to_request):
                request = future_to_request[future]
                try:
                    results.append(future.result())
                except Exception as e:
                    log.error(f"Request {request} failed: {e}")
        return results


class SupersetApi(_SupersetApiBase):
    """
    Class for interacting with the Superset API.
    Provides methods for making requests and performing common operations.
    """

    def request(
        self, method: HTTPMethod, endpoint: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Make a request to the Superset API.

        :param method: The HTTP method to use for the request.
        :param endpoint: The API endpoint to request.
        :param kwargs: Additional arguments to pass to the request.
        :return: The JSON response from the API.
        """
        return self._request(method, endpoint, **kwargs)

    def parallel_requests(
        self, requests_list: List[Tuple[HTTPMethod, str, Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """
        Make multiple requests to the Superset API in parallel.

        :param requests_list: A list of tuples containing the HTTP method, endpoint, and arguments for each request.
        :return: A list of JSON responses from the API.
        """
        return self._parallel_requests(requests_list)

    def get_database_id(self, database_name: str) -> Union[int, None]:
        """
        Get the ID of a database by its name.

        :param database_name: The name of the database.
        :return: The ID of the database, or None if not found.
        """
        try:
            response = self.request(HTTPMethod.GET, "/database/")
            databases = response["result"]
            for db in databases:
                if db.get("database_name") == database_name:
                    return db.get("id")
        except Exception as e:
            log.error(f"Failed to get database ID for {database_name}: {e}")
        return None

    def upload_csv_to_database(
        self,
        database_id: int,
        table_name: str,
        csv_data: str,
        schema: str = "public",
        column_dates: List[str] = None,
        overwrite: bool = True,
    ) -> Dict[str, Any]:
        """
        Upload a CSV file to a database.

        :param database_id: The ID of the database.
        :param table_name: The name of the table to create or overwrite.
        :param csv_data: The CSV data to upload.
        :param schema: The schema of the table.
        :param column_dates: A list of columns to treat as dates.
        :param overwrite: Whether to overwrite the table if it already exists.
        :return: The JSON response from the API.
        """
        files = {
            "already_exists": (None, "replace" if overwrite else "fail"),
            "table_name": (None, table_name),
            "schema": (None, schema),
            "file": ("data.csv", csv_data),
        }

        if column_dates:
            files["column_dates"] = (None, ",".join(column_dates))

        try:
            return self.request(
                HTTPMethod.POST, f"/database/{database_id}/csv_upload/", files=files
            )
        except Exception as e:
            log.error(f"Failed to upload CSV to database {database_id}: {e}")
            raise

    def get_dataset_id(self, dataset_name: str) -> Union[int, None]:
        """
        Get the ID of a dataset by its name.

        :param dataset_name: The name of the dataset.
        :return: The ID of the dataset, or None if not found.
        """
        try:
            response = self.request(HTTPMethod.GET, "/dataset/")
            datasets = response["result"]
            for dataset in datasets:
                if dataset.get("table_name") == dataset_name:
                    return dataset.get("id")
        except Exception as e:
            log.error(f"Failed to get dataset ID for {dataset_name}: {e}")
        return None

    def create_dataset(
        self,
        database_id: int,
        table_name: str,
        schema: str,
        owners: List[int],
        sql: str = None,
    ) -> Dict[str, Any]:
        """
        Create a new dataset.

        :param database_id: The ID of the database.
        :param table_name: The name of the table.
        :param schema: The schema of the table.
        :param owners: A list of owner IDs.
        :param sql: The SQL query to use for the dataset.
        :return: The JSON response from the API.
        """
        if sql is None:
            sql = f"SELECT * FROM {schema}.{table_name}"
        payload = {
            "always_filter_main_dttm": False,
            "catalog": "",
            "database": database_id,
            "external_url": "",
            "is_managed_externally": True,
            "normalize_columns": False,
            "owners": owners,
            "schema": schema,
            "sql": sql,
            "table_name": table_name,
        }
        try:
            return self.request(HTTPMethod.POST, "/dataset/", json=payload)
        except Exception as e:
            log.error(f"Failed to create dataset for table {table_name}: {e}")
            raise
