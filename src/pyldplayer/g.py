from .core.config import ConfigCollection
from .core.g import Global
from .core.mapping import MappingCollection
from .core.path import LDPath
from .core.record import RecordCollection
from .core.console import Console


path = LDPath.auto()
record = RecordCollection.auto()
mapping = MappingCollection.auto()
config = ConfigCollection.auto()
console = Console.auto() 