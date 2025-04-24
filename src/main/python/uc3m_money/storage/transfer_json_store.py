from uc3m_money import TRANSFERS_STORE_FILE, AccountManagementException


class TransferJsonStore():
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

