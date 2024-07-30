

import logging
import os
import sys
from pyldplayer.core.console import Console
from pyldplayer.core.g import Global

Global(os.environ["LDPLAYER_PATH"])
c = Console.auto()

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

# ✅
#c.launch(index=2)
w = c.list2()

from pyldplayer.g import config
# ✅
#x = config.default_config()

pass