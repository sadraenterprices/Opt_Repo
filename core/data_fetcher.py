import requests

class TSEDataFetcher:
    def __init__(self):
        self.base_url = "https://api.tse.ir/api/OptionChain"  # Example API endpoint

    def fetch_option_chain(self):
        """
        Fetches real-time option chain data from Tehran Stock Exchange.
        :return: JSON response containing option chain data.
        """
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()  # Returning the JSON response
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

if __name__ == "__main__":
    fetcher = TSEDataFetcher()
    data = fetcher.fetch_option_chain()
    if data:
        print(data)
