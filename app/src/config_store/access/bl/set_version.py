from config_store.access.dal.set_version import FacadeSetVersion
class SetVersion:
    @staticmethod
    def get_all_latest_set_version(self):
        return FacadeSetVersion.get_all_latest_set_version(self)
