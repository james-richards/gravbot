gravbot
=======

LOREM IPSUM TROLOLOLEM


dev stuff
---------

### profiling

    I've rigged `launch.py` to run `gravbot/mc.py` optionally with profiling. E.g.:

        python launch.py --profile    

    The profiling output is spammed to stdout if you quit the game via ESC or hit ctrl+C.

### fixing broken indentation

    script to normalise all indentation to use 4-space tabs: [reindent.py](http://svn.python.org/view/python/trunk/Tools/scripts/reindent.py?revision=66903&view=markup)

### pylint

    probably not a bad idea to run `pylint -E` over code before comitting

