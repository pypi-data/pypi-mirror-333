# An easier brython library

This is library to use brython (document, window, etc) without breaking brain<br>

## FAQ <br>

1. Q: Why this library even exists? What was a reason of creating?<br>
A: One time, i was creating a game on brython, but using window.localstorage was too hard, so i created this library. Later, I've got a one more idea, then one more, then more, and that how it grown up. <br>
2. Q: How to use it?<br>
A: Two ways, one if you need to full, other if you want a few functions.<br>
First way:

```python
from brython_easier import *
```

Second way:

```python
from brython_easier import LocalStorageManager, timers  # and_etc
```

3. Q: Why not use brython directly?<br>
A: You can use it, but it's a bit too hard to use. If you want to use it, use as you want, you can even both import in the same time. This library created to make brython more simple
4. Q: My code giving me ValueError, Storage name is not set, how to fix it?<br>
A: Use set_storage function to set the storage name, For example:
```python
localstorage.set_storage("ExampleGame") # put it somewhere in the start of code
```

5. Q: How to install library?<br>
A: Use pip install brython-easier, or you can just download file and import like that:
```python
from your_file_name import *
```

6. Q: How to contribute?<br>
A: It's very simple, just create a pull request, and i'll look in it
7. Q: How to report a bug?<br>
A: Create an issue