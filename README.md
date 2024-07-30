# pyldplayer
## Overview
This project is a reborn version after being archived. It serves as a base command-line and folder structure wrapper for LDPlayer, with no additional dependencies. For extended features, please see [reldplayer](https://github.com/ZackaryW/reldplayer).

## Installation
```bash
pip install pyldplayer
```

## Features
provides abstraction for 
* record - macros
* console - commandline interface
* config - configuration located at `app/vm`
* mapping - SMP and KMP (keyboard mapping) files

`g` is a submodule that allows quick initialization of a single global instance
```py
import pyldplayer.g as g
g.Global({path})
g.record : RecordCollection
g.mapping : MappingCollection
g.config : ConfigCollection
g.console : Console
```
