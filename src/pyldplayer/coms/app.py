
from functools import lru_cache
import glob
import os
from pyldplayer.coms.appattr import ContainLDAppAttrI, LDAppAttr
from pyldplayer.model.LeidiansConfig import LeidiansConfig
from pyldplayer.model.LeidianConfig import LeidianConfig
from pyldplayer.model.kmp import KeyboardMappingFile
from pyldplayer.model.record import LDRecord
from pyldplayer.model.smp import SMPFile

class Flags:
    RECORD = 1
    KMP = 2
    SMP = 3
    CONFIG = 4
    CUSTOM = 5
    RECOMMENDED = 6

class LDApp(ContainLDAppAttrI):
    """
    A wrapper class for managing the LDPlayer folder structure and file access.
    
    This class provides an interface to access and query different types of files
    in the LDPlayer directory structure, including:
    - Operation records (.record files)
    - Keyboard mapping profiles (.kmp files)
    - Screen mapping profiles (.smp files) 
    - VM configurations (.config files)

    Files can be accessed from either the custom or recommended directories where applicable.
    
    Attributes:
        _RECORD (int): Constant for record file type
        _KMP (int): Constant for keyboard mapping file type
        _SMP (int): Constant for screen mapping file type
        _CONFIG (int): Constant for config file type
        _CUSTOM (int): Constant for custom directory
        _RECOMMENDED (int): Constant for recommended directory
    """
    _RECORD = 1
    _KMP = 2
    _SMP = 3
    _CONFIG = 4
    _CUSTOM = 5
    _RECOMMENDED = 6

    def __init__(self, attr : LDAppAttr = None):
        """
        Initialize the LDApp instance.

        Args:
            attr (LDAppAttr, optional): LDPlayer application attributes. If None, default will be used.
        """
        ContainLDAppAttrI.__init__(self, attr)
    
    def query_record(self, key : str, partial : bool = False):
        """
        Query operation record files.

        Args:
            key (str): The name or pattern to search for
            partial (bool): If True, performs partial matching with wildcards

        Returns:
            list[LDRecord]: List of matching record objects
        """
        if partial:
            key = f"*{key}*"
        return self[self._RECORD, key]

    def query_kmp(self, key : str, partial : bool = False, recommended : bool = False):
        """
        Query keyboard mapping profile files.

        Args:
            key (str): The name or pattern to search for
            partial (bool): If True, performs partial matching with wildcards
            recommended (bool): If True, searches in recommended configs instead of custom

        Returns:
            list[KeyboardMappingFile]: List of matching KMP objects
        """
        if partial:
            key = f"*{key}*"
        if recommended:
            return self[self._KMP, self._RECOMMENDED, key]
        else:
            return self[self._KMP, self._CUSTOM, key]

    def query_smp(self, key : str, partial : bool = False, recommended : bool = False):
        """
        Query screen mapping profile files.

        Args:
            key (str): The name or pattern to search for
            partial (bool): If True, performs partial matching with wildcards
            recommended (bool): If True, searches in recommended configs instead of custom

        Returns:
            list[SMPFile]: List of matching SMP objects
        """
        if partial:
            key = f"*{key}*"
        if recommended:
            return self[self._SMP, self._RECOMMENDED, key]
        else:
            return self[self._SMP, self._CUSTOM, key]
        
    def query_config(self, key : int):
        """
        Query VM configuration files.

        Args:
            key (int): The VM index to search for

        Returns:
            list[LeidianConfig]: List of matching config objects
        """
        return self[self._CONFIG, f"{key}"]
        

    @lru_cache
    def _query_types(self, *keys):
        """
        Internal method to validate and process query type parameters.

        Args:
            *keys: Variable length argument list with the last item being the search string

        Returns:
            tuple: Query type and config type (custom/recommended)

        Raises:
            ValueError: If the query parameters are invalid
        """
        # assert last key is string
        assert isinstance(keys[-1], str), "Last key must be a string"
        ctype = "custom"
        qtype = None
        repeat : int = 0
        repeat2 : int = 0
        for key in keys[:-1]:
            if key in [self._RECORD, self._KMP, self._SMP, self._CONFIG]:
                qtype = key
                repeat += 1
            elif key in [self._CUSTOM, self._RECOMMENDED]:
                ctype = "custom" if key == self._CUSTOM else "recommended"
                repeat2 += 1
            else:
                raise ValueError(f"Invalid key: {key}")
        
        if repeat > 1:
            raise ValueError("Only one of RECORD, KMP, SMP, CONFIG is allowed")
        if repeat2 > 1:
            raise ValueError("Only one of CUSTOM, RECOMMENDED is allowed")

        if qtype not in [self._KMP, self._SMP] and repeat2 >= 1:
            raise ValueError("CUSTOM and RECOMMENDED can only be used with KMP and SMP")

        if qtype is None:
            raise ValueError("No query type specified")

        return qtype, ctype

    @lru_cache
    def _query_targetPath(self, *keys):
        """
        Internal method to determine target path and filename pattern for queries.

        Args:
            *keys: Query parameters

        Returns:
            tuple: Target folder path and filename pattern
        """
        qtype, ctype = self._query_types(*keys)

        match qtype:
            case self._RECORD:
                return self.attr.operationRecords, "{name}.record"
            case self._KMP | self._SMP if ctype == "custom":
                return self.attr.customizeConfigs, "{name}.{type}".replace("{type}", "kmp" if qtype == self._KMP else "smp")
            case self._KMP | self._SMP if ctype == "recommended":
                return self.attr.recommendedConfigs, "{name}.{type}".replace("{type}", "kmp" if qtype == self._KMP else "smp")
            case self._CONFIG:
                return self.attr.config, "leidian{name}.config"
    
    def _query(self, *keys):
        """
        Internal method to execute queries and yield matching file objects.

        Args:
            *keys: Query parameters

        Yields:
            Union[LDRecord, KeyboardMappingFile, SMPFile, LeidianConfig]: Matching file objects

        Raises:
            FileNotFoundError: If exact match is requested but file not found
        """
        targetfolder, targetfname = self._query_targetPath(*keys)
        qtype, _ = self._query_types(*keys)

        if "*" not in keys[-1]:
            if not os.path.exists(os.path.join(targetfolder, targetfname.format(name=keys[-1]))):
                raise FileNotFoundError(f"File {keys[-1]} not found")
            eligibleFiles = [os.path.join(targetfolder, targetfname.format(name=keys[-1]))]
        eligibleFiles = glob.glob(os.path.join(targetfolder, targetfname.format(name=keys[-1])))

        for file in eligibleFiles:
            match qtype:
                case self._RECORD:
                    yield LDRecord.load(file)
                case self._KMP:
                    yield KeyboardMappingFile.load(file)
                case self._SMP:
                    yield SMPFile.load(file)
                case self._CONFIG:
                    if file.endswith("leidians.config"):
                        continue
                    yield LeidianConfig.load(file)


    def __getitem__(self, *keys):
        """
        Implements dictionary-style access to query files.

        Args:
            *keys: Query parameters, either as separate arguments or a tuple

        Returns:
            list: List of matching file objects
        """
        if isinstance(keys[-1], tuple):
            keys = keys[0]
            
        return list(self._query(*keys))
    
    def leidiansConfig(self):
        """
        Get the global LDPlayer configuration.

        Returns:
            LeidiansConfig: The global configuration object
        """
        return LeidiansConfig.load(os.path.join(self.attr.config, "leidians.config"))
