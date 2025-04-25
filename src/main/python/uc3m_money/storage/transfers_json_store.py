"""transfers_json_store"""
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.storage.json_store import JsonStore
from uc3m_money.account_management_config import TRANSFERS_STORE_FILE


class TransfersJsonStore(JsonStore):
    _file_name = TRANSFERS_STORE_FILE

    def add_item(self, item):
        """add item"""
        for transfer in self._data_list:
            if (transfer == item.to_json()):
                raise AccountManagementException("Duplicated transfer in transfer list")
        super().add_item(item)



"""
    class __TransferJsonStore(JsonStore):
        _file_name =TRANSFERS_STORE_FILE

        def add_item(self,item):
            self.load_list_from_file()
            for old_transfer in self._data_list:
                if old_transfer == item.to_json():
                    raise AccountManagementException("Duplicated transfer in transfer list")
                super().add_item(item)
    instance = None

    def __new__(cls):
        if not TransferJsonStore.instance:
            TransferJsonStore.instance = TransferJsonStore.__TransferJsonStore()
        return TransferJsonStore.instance


    def __getattr__(self, item):
        return getattr(TransferJsonStore.instance, item)

    def __setattr__(self, key, value):
        return setattr(TransferJsonStore.instance, key, value)


"""