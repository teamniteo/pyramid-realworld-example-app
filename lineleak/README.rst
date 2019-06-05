LINELEAK
========

Introduction
------------

If your script has more than a set number of lines, your code lines are leaking :).

Lineleak is a ``flake8`` plugin that counts the lines containing live code in a script, and 'yells' if a set limit is exceeded.
It is meant to help enforce short scripts and modular python programming.

For usefulness, lineleak only counts lines which contains live code. Thus the following lines are excluded from a count.
- Blank lines
- Comment lines
- Lines of a docstring 


Usage 
-----
To benefit from ``lineleak``, Use flake8 the usual way with plugins::

    $ flake8 [options] file ... 

The default line count limit is set at 500, and imposed on physical lines. These defaults, however, can be overridden with optional arguments as shown below and illustrated in the illustration section::


    optional arguments:
    
      --lineleak-logical           Applies line count limit to logical lines.
  
      --max-line-count=MAX_LINE_COUNT
                          Changes the maximum limit for live code line count.
                          
      --live-code-count     Displays the number of physical and logical lines 
                            containing live code.
                        

Codes
-----
* ``LLW404`` Reports that logical line count has exceeded limit
* ``LLW405`` Reports that physical line count has exceeded specified limit
* ``LLI200`` Informs about the number of logical and physical lines containing live code.

Illustration
------------
a. Overriding default line count limit (limit -> 500)::

    $ flake8 --max-line-count=50 lineleak.py
    linesleak.py:82:1: LLW405 Maximum number of physical live code lines (50) exceeded.

b. Imposing limit on logical, instead of physical, lines::

    $ flake8 --lineleak-logical linesleak.py
    linesleak.py:103:1: LLW404 Maximum number of logical live code lines (50) exceeded.

c. Doing both (a) and (b)::

    $ flake8 --max-line-count=40 --lineleak-logical linesleak.py
    linesleak.py:84:1: LLW404 Maximum number of logical live code lines (40) exceeded.

d. Display number of lines containing live code::

    $ flake8 --live-code-count linesleak.py
    linesleak.py:118:1: LLI200 [INFO] Live code count: 56 logical and 79 physical lines

e. Ignore limit enforcement.
In adherence with flake8 design principles, lineleak can be silenced by adding the appropriate error codes of lineleak to the ignore list::

    $ flake8 --ignore=LL linesleak.py
    $

Environment
-----------
* Shell

Dependencies & Compatibility
----------------------------
* Best suited for `flake8` 3.3 - 3.6
* Not compatible with `flake8` >= 3.7, due to an issue related to the OptionManager conflict handling.
* No external libraries required currently

Software Cycle Stage
--------------------
* Development
