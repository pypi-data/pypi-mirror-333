from typing import Optional, Type
from snakemake_interface_storage_plugins.tests import TestStorageBase
from snakemake_interface_storage_plugins.storage_provider import StorageProviderBase
from snakemake_interface_storage_plugins.settings import StorageProviderSettingsBase
from snakemake_storage_plugin_orcestra import StorageProvider, StorageProviderSettings

class TestStorage(TestStorageBase):
    __test__ = True
    # set to True if the storage is read-only
    retrieve_only = True
    # set to True if the storage is write-only
    store_only = False
    # set to False if the storage does not support deletion
    delete = False
    # set to True if the storage object implements support for touching (inherits from
    # StorageObjectTouch)
    touch = False
    # set to False if also directory upload/download should be tested (if your plugin
    # supports directory down-/upload, definitely do that)
    files_only = True

    def get_query(self, tmp_path) -> str:
        # Return a query. If retrieve_only is True, this should be a query that
        # is present in the storage, as it will not be created.
        return "orcestra://pharmacosets/GRAY_2013"

    def get_query_not_existing(self, tmp_path) -> str:
        # Return a query that is not present in the storage.
        return "orcestra://pharmacosets/CCLE_2015_not_existing"

    def get_storage_provider_cls(self) -> Type[StorageProviderBase]:
        # Return the StorageProvider class of this plugin
        return StorageProvider

    def get_storage_provider_settings(self) -> Optional[StorageProviderSettingsBase]:
        # instantiate StorageProviderSettings of this plugin as appropriate
        return StorageProviderSettings()
