# pyldplayer
a python wrapper for LDPlayer

## Installation
```bash
pip install pyldplayer
```

to install an older version, use
```bash
pip install pyldplayer==3.0.6
```

## About
This project went through several major reworks. 
Initially, it was a simple wrapper for the commandline and nothing else.
Later, Windows API and autogui related functions were added.
Considering the project was becoming more and more bloated, a new project [reldplayer](https://github.com/ZackaryW/reldplayer) was added to host those functions.
This project now contains no additional dependencies but it has all the necessary implementations for extension.

## Usage
### 1. to initialize
#### 1.1 via os.environ
```py
import os
os.environ["LDPLAYER_PATH"] = "path"
appattr = LDAppAttr()
```
#### 1.2 via direct initialization
```py
appattr = LDAppAttr(path)
```

### 2. using console commands
```py
console = LDConsole()
console.launch(name="test")
console.reboot(index=1)
console.quitall()
```
### 3. getting meta documents
```py
app = LDApp()
# to get a list of documents in recommendedconfig
os.listdir(app.attr.recommendedConfigs)

# query
smpobj = app[Flags.RECOMMENDED, Flags.SMP, "some query"] 
```

### 4. execute batch commands
```py
from pyldplayer import LDConsole

console = LDBatchConsole()
console.add_interval() # this adds a sleep interval
console.launch([1,2,3])
```