
import pytest

from pyldplayer.coms.app import Flags, LDApp
from pyldplayer.coms.appattr import LDAppAttr




def test_same_instance():
    
    from pyldplayer.coms.batchConsole import LDBatchConsole
    from pyldplayer import LDConsole


    console = LDBatchConsole()
    console.add_interval()

    console2 = LDConsole()

    assert console2 is console._LDBatchConsole__console

@pytest.mark.skip
def test_init_via_environ():
    import os
    os.environ["LDPLAYER_PATH"] = "path"
    appattr = LDAppAttr()

def test_2():
    app = LDApp()
    app[Flags.RECOMMENDED, Flags.SMP, "some query"]
