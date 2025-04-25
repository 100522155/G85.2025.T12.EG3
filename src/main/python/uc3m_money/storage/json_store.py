"""JsonStore definition"""
import json
from uc3m_money.account_management_exception import AccountManagementException


""""""

class JsonStore():
    """JsonStore class"""

    _data_list = []
    _file_name = ""

    def __init__(self):
        self.load_list_from_file()

    def save_list_to_file(self):
        """Saves the list in the store"""
        try:
            with open(self._file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file or file path") from ex

    def load_list_from_file(self):
        """load the list of items from the store"""
        try:
            with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            self._data_list = []
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode error - Wrong JSON Format") from ex

    def add_item(self, item):
        """add a new item in the store"""
        self.load_list_from_file()
        self._data_list.append(item.to_json())
        self.save_list_to_file()
