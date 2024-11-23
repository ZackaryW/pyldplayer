from dataclasses import dataclass
import re
import typing

from pyldplayer.model.list2meta import List2Meta

@dataclass(slots=True)
class Cond:
    def __init__(self, *args):
        self.conds = args

    def validate(self, meta : List2Meta):
        for cond in self.conds:
            assert isinstance(cond, str)
            if not eval(cond, meta):
                return False
        return True

@dataclass(slots=True) 
class QueryObj:
    """
    QueryObj is a flexible query object for filtering LDPlayer instances based on different criteria.
    
    It supports the following query types:
    - String matching: Match emulator name exactly or with pattern (using *)
    - ID range: Match emulators with IDs in a given range (tuple of start,end)
    - ID list: Match specific emulator IDs from a list
    - Conditional: Match based on custom conditions using Cond class
    
    Examples:
        QueryObj("ldplayer-1")  # Match exact name
        QueryObj("ldplayer-*")  # Pattern match with wildcard
        QueryObj((0,5))         # Match IDs 0-5
        QueryObj([1,3,5])       # Match IDs 1, 3 or 5
        QueryObj(Cond("id < 5")) # Match condition
        QueryObj([1, "ldplayer-1", "*l]) # Match ID 1 or name "ldplayer-1" or regex
    """
    string : str = None
    isPattern : bool = False
    range : typing.Tuple[int, int] = None
    lists : typing.List[typing.Union[str, int]] = None
    cond : Cond = None

    @classmethod
    def parse(cls, query : typing.Any):
        if isinstance(query, QueryObj):
            return query

        if isinstance(query, str):
            if "*" in query:
                return cls(string=query, isPattern=True)
            return cls(string=query)
        
        if isinstance(query, int):
            return cls(lists=[query])
        
        if isinstance(query, tuple) and len(query) == 2:
            return cls(range=query)
        
        if isinstance(query, list) and all(isinstance(item, (str, int)) for item in query):
            return cls(lists=query)
        
        if isinstance(query, Cond):
            return cls(cond=query)

        raise ValueError(f"Invalid query: {query}")
    
    def validate(self, meta : List2Meta):
        if self.string:
            if self.isPattern:
                return re.match(self.string, meta["name"]) is not None

            return self.string == meta["name"]
    
        if self.range:
            return self.range[0] <= meta["id"] <= self.range[1]
        
        if self.lists:
            for item in self.lists:
                if meta["id"] == item:
                    return True
                if not isinstance(item, str):
                    continue
                if meta["name"] == item:
                    return True
                if "*" in item:
                    if re.match(item, meta["name"]):
                        return True

        
        if self.cond:
            return self.cond.validate(meta)
        
        return False
