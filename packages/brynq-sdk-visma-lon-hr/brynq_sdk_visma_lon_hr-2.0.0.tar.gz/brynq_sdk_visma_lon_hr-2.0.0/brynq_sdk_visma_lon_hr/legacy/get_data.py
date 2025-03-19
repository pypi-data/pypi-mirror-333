import warnings
from typing import Union, List
import pandas as pd
import requests
import xmltodict
from brynq_sdk_brynq import BrynQ


class GetData(BrynQ):
    """
    DEPRECATED: Use Visma class instead.
    A class to fetch data from Visma Lon HR API.
    """

    def __init__(self, label: Union[str, List], debug: bool = False):
        """
        Initialize the GetData class.

        Args:
            label (Union[str, List]): The label or list of labels to get the credentials.
            debug (bool): Flag to enable debug mode. Defaults to False.
        """
        warnings.warn(
            "GetData class is deprecated. Use Visma class instead",
            DeprecationWarning,
            stacklevel=2
        )

        super().__init__(label, debug)
        self.api_key = self._set_credentials(label)
        self.url = "https://datahub.vismaenterprise.dk/datahub/V2/mainservice.svc/"

    def _set_credentials(self, label) -> str:
        """
        Retrieve API key from the system credentials.

        Args:
            label (Union[str, List]): The label or list of labels to get the credentials.

        Returns:
            str: The API key.
        """
        credentials = self.get_system_credential(system='visma-lon-hr', label=label)
        api_key = credentials['api_key']
        return api_key

    def get_data(self, table_name: str, filter: str = None) -> pd.DataFrame:
        """
        Fetch data from a specified table in Visma Lon HR.

        This method constructs a request URL based on the table name and optional filter,
        sends a request to the Visma Lon HR API, parses the XML response, and converts it
        to a pandas DataFrame. The DataFrame columns are cleaned to remove unnecessary
        characters and duplicate columns are handled.

        Args:
            table_name (str): The name of the table to fetch data from.
            filter (str, optional): The filter to apply to the data fetch. Defaults to None.

        Returns:
            pd.DataFrame: The fetched data as a pandas DataFrame.
        """
        # Initial URL with subscription-key
        base_url = f"{self.url}{table_name}?"
        # Apply the filter if provided
        if filter:
            base_url += f"$filter={filter}&"
        # Append subscription-key
        base_url += f"subscription-key={self.api_key}"

        all_data = []

        while True:
            response = requests.get(base_url)
            if response.status_code == 200:
                data_dict = xmltodict.parse(response.content)
                entries = data_dict['feed'].get('entry', [])
                if isinstance(entries, dict):
                    entries = [entries]  # Ensure entries is a list
                table_data = []
                for entry in entries:
                    if 'content' in entry and 'm:properties' in entry['content']:
                        table_data.append(entry['content']['m:properties'])
                all_data.extend(table_data)

                # Check for next link
                next_link = None
                links = data_dict['feed'].get('link', [])
                if isinstance(links, list):
                    for link in links:
                        if link['@rel'] == 'next':
                            next_link = link['@href']
                            base_url = f"{next_link}&subscription-key={self.api_key}"
                            break
                elif isinstance(links, dict) and links['@rel'] == 'next':
                    next_link = links['@href']
                    base_url = f"{next_link}&subscription-key={self.api_key}"
                if not next_link:
                    break
            else:
                response.raise_for_status()

        # Normalize the nested dictionary
        df = pd.json_normalize(all_data)

        # Drop all type fields and xml:space fields
        df = df[df.columns.drop(list(df.filter(regex='@m:type|xml:space')))]

        # Clean column names by removing unwanted characters
        df.columns = [col.replace('d:', '').replace('.#text', '').replace('.@m:null', '').replace('@m:null', '') for col
                      in df.columns]

        # Extract text from nested dictionaries
        df = df.applymap(lambda x: x['#text'] if isinstance(x, dict) and '#text' in x else x)

        # Handle duplicate column names
        df = df.loc[:, ~df.columns.duplicated()]

        return df