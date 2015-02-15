Introduction
============

PyZ80 is a Z80 cpu emulator written entirely in Python.
Currently the code is being heavily refactored to use
proper object oriented abstractions.

This project relies on the SimpleFSM module which is not
available on PyPI and can be found `here <https://github.com/lliendo/SimpleFSM>`_

At the moment only a few tests are green and the code itself is not able
to execute any full program. A few remaining instructions and a battery of
unit tests are under development.

Installation
------------

It is strongly recommended to use a fresh `virtualenv <https://virtualenv.pypa.io/en/latest/>`_.
Clone and install SimpleFSM mentioned above and if you're using a virtualenv, activate it.

.. code-block:: bash
    
    $ git clone https://github.com/lliendo/SimpleFSM.git
    $ cd SimpleFSM
    $ python setup.py install

Get PyZ80 (but don't install it as this is still working in progress).

.. code-block:: bash
    
    $ git clone https://github.com/lliendo/PyZ80.git
    $ cd PyZ80


Running PyZ80
-------------

Go to the cloned PyZ80 directory and run the 'run-pyz80' script.

.. code-block:: bash
    
    $ cd /path/to/cloned/PyZ80
    $ ./run-pyz80 -h

The above command should display all available options.
By default programs are loaded to 0x00 but you can override
this by specifying the -a option (which takes an hexadecimal address).

Device support hasn't been tested yet altough all logic to attach and 
run them is developed.

Keep in mind that this is a hobby project and is inteded to understand how
an emulator works and also how it can be developed using a modern
programming language such as Python. Currently many instructions may be
buggy and some of them may not work at all.
