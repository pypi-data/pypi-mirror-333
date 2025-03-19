import requests
import json
import os

from common_utils.logger import create_logger


class FirebaseClient:
    log = create_logger("FirebaseClient")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    def __init__(self, realtime_db_url: str | None = None):
        """Firebase client to interact with a realtime database

        Currently only supports unauthenticated access."""
        self.database_url = realtime_db_url or os.getenv("FIREBASE_REALTIME_DB_URL")
        if not self.database_url:
            raise ValueError("Could not load firebase project from environment variables")

    def get_list(self, ref: str, max_results: int = 100, convert_to_list: bool = True):
        """Get a list of child-entries from an object in firebase."""
        params = {"orderBy": '"$key"', "limitToFirst": str(max_results)}
        reference_url = f"{self.database_url}/{ref}.json"
        try:
            response = requests.get(url=reference_url, params=params)
            self.log.debug(f"Getting List: {response.text}")
            if convert_to_list:
                list_json = response.json()
                return [list_json[key] for key in list_json]
            else:
                return response.json()
        except Exception as e:
            self.log.error(f"Failed to get list from {ref}: {e}")
            return None

    def delete_entry(self, ref: str):
        """Delete an object entry from firebase"""
        try:
            requests.delete(url=f"{self.database_url}/{ref}.json")
            self.log.debug(f"Deleted entry {ref} from firebase")
        except Exception as e:
            self.log.error(f"Failed to delete entry {ref}: {e}")

    def get_entry(self, ref: str):
        """Get an object entry from firebase"""
        try:
            response = requests.get(url=f"{self.database_url}/{ref}.json").json()
            self.log.debug(f"Got entry {ref} from firebase: {response}")
            return response
        except Exception as e:
            self.log.error(f"Failed to get entry {ref}: {e}")
            return None

    def set_entry(self, ref: str, data: dict):
        """Set an object entry in firebase"""
        try:
            url = f"{self.database_url}/{ref}.json"
            response = requests.put(url=url, headers=self.headers, data=json.dumps(data))
            self.log.debug(f"Set entry {ref} with data {data} in firebase: {response.text}")
        except Exception as e:
            self.log.error(f"Failed to set entry {ref}: {e}")


if __name__ == "__main__":
    firebase = FirebaseClient()
