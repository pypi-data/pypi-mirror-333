import logging
import uuid
from typing import Literal

import pandas as pd

from .SupersetApi import SupersetApi

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

log = logging.getLogger()


class DataFrameToSuperset:
    """
    A class to upload pandas DataFrames to Superset.

    Attributes:
        superset_api (SupersetApi): An instance of the SupersetApi class.
        schema (str): The schema name in the database.
        base_url (str): The base URL of the Superset instance.
        database_id (int): The ID of the database in Superset.
        database_name (str): The name of the database in Superset.
    """

    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        provider: Literal["ldap", "db"],
        database_name: str,
        schema: str = "public",
    ):
        """
        Initializes the DataFrameToSuperset with Superset credentials and database details.

        Args:
            base_url (str): The base URL of the Superset instance.
            username (str): The username for Superset authentication.
            password (str): The password for Superset authentication.
            provider (Literal["ldap", "db"]): The authentication provider.
            database_name (str): The name of the database in Superset.
            schema (str, optional): The schema name in the database. Defaults to "public".

        Raises:
            ValueError: If the database with the given name is not found.
            Exception: If there is an error during initialization.
        """
        self.superset_api = SupersetApi(base_url, username, password, provider)
        self.schema = schema
        self.base_url = base_url

        try:
            database_id = self.superset_api.get_database_id(database_name)
            if database_id is None:
                raise ValueError(f"Database with name '{database_name}' not found.")
            self.database_id = database_id
            self.database_name = database_name
        except Exception as e:
            log.error(f"Error initializing DataFrameToSuperset: {e}")
            raise

    def _upload_dataframe(self, dataframe: pd.DataFrame, name: str = None) -> dict:
        """
        Uploads a pandas DataFrame to Superset as a CSV.

        Args:
            dataframe (pd.DataFrame): The DataFrame to upload.
            name (str, optional): The name of the dataset in Superset. Defaults to None.

        Returns:
            dict: The response from the Superset API.

        Raises:
            Exception: If there is an error during the upload.
        """
        try:
            csv_data = dataframe.to_csv(index=False)
            date_columns = [
                col
                for col in dataframe.columns
                if pd.api.types.is_datetime64_any_dtype(dataframe[col])
            ]
            response = self.superset_api.upload_csv_to_database(
                self.database_id,
                name,
                csv_data,
                schema=self.schema,
                column_dates=date_columns,
            )
            return response
        except Exception as e:
            log.error(f"Error uploading DataFrame: {e}")
            raise

    def to_superset(
        self, dataframe: pd.DataFrame, name: str = None, verbose_return: bool = False
    ) -> dict:
        """
        Uploads a DataFrame to Superset and returns the dataset URL or details.

        Args:
            dataframe (pd.DataFrame): The DataFrame to upload.
            name (str, optional): The name of the dataset in Superset. Defaults to generated name.
            verbose_return (bool, optional): If True, returns detailed information. Defaults to False.

        Returns:
            dict: The dataset URL or detailed information.

        Raises:
            ValueError: If the dataset ID cannot be retrieved.
            Exception: If there is an error during the upload.
        """
        if name is None:
            name = f"{self.superset_api.username}_generated_dataset_{uuid.uuid4().hex}"
            log.warning(
                f"No name provided, using generated '{name}' as name. May clutter the database ({self.database_name}) datasets list."
            )
        try:
            self._upload_dataframe(dataframe, name)
            dataset_id = self.superset_api.get_dataset_id(name)
            if dataset_id is None:
                raise ValueError(f"Failed to retrieve dataset ID for '{name}'")
            url = f"{self.base_url}/explore/?datasource_type=table&datasource_id={dataset_id}"
            log.debug(f"Dataset uploaded successfully: {name}")
            log.info(f"Explore the dataset at: {url}")
            if verbose_return:
                return {"dataset_id": dataset_id, "name": name, "url": url}
            else:
                return url
        except Exception as e:
            log.error(f"Error in to_superset: {e}")
            raise


def upload_dataframe_to_superset(
    dataframe: pd.DataFrame,
    base_url: str,
    username: str,
    password: str,
    provider: Literal["ldap", "db"],
    database_name: str,
    schema: str = "public",
    name: str = None,
    verbose_return: bool = False,
) -> dict:
    """
    Uploads a pandas DataFrame to Superset without needing to create a DataFrameToSuperset object.

    Args:
        dataframe (pd.DataFrame): The DataFrame to upload.
        base_url (str): The base URL of the Superset instance.
        username (str): The username for Superset authentication.
        password (str): The password for Superset authentication.
        provider (Literal["ldap", "db"]): The authentication provider.
        database_name (str): The name of the database in Superset.
        schema (str, optional): The schema name in the database. Defaults to "public".
        name (str, optional): The name of the dataset in Superset. Defaults to generated name.
        verbose_return (bool, optional): If True, returns detailed information. Defaults to False.

    Returns:
        dict: The dataset URL or detailed information.

    Raises:
        ValueError: If the dataset ID cannot be retrieved.
        Exception: If there is an error during the upload.
    """
    uploader = DataFrameToSuperset(
        base_url, username, password, provider, database_name, schema
    )
    return uploader.to_superset(dataframe, name, verbose_return)


def monkey_patch_to_allow_df_to_superset(
    base_url: str,
    username: str,
    password: str,
    provider: Literal["ldap", "db"],
    database_name: str,
    schema: str = "public",
    default_name: str = None,
):
    """
    Adds a to_superset method to pandas DataFrame class with predefined Superset credentials and database details.

    Args:
        base_url (str): The base URL of the Superset instance.
        username (str): The username for Superset authentication.
        password (str): The password for Superset authentication.
        provider (Literal["ldap", "db"]): The authentication provider.
        database_name (str): The name of the database in Superset.
        schema (str, optional): The schema name in the database. Defaults to "public".
        name (str, optional): The name of the dataset in Superset. Defaults DataFrame's name else to generated name.
    """

    def to_superset(self, name: str = None, verbose_return: bool = False):
        dataset_name = name or self.name or default_name
        return upload_dataframe_to_superset(
            self,
            base_url,
            username,
            password,
            provider,
            database_name,
            schema,
            dataset_name,
            verbose_return,
        )

    pd.DataFrame.to_superset = to_superset
