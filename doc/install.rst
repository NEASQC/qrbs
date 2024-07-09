Install
=======

In this section we explain how to install the neasqc-qrbs package in Python. We recommend the use of `Python virtual environments <https://docs.python.org/3/tutorial/venv.html>`_ to work with this package, in order to not disturb other work you might be doing. 

Once that has been taken care of, you can proceed with the installation! The first step will be to clone the repository:

..  code::

    git clone https://github.com/NEASQC/qrbs


Once you have cloned the project, go to its directory and make sure your Python virtual environment is activated. Here we present two methods to install the package, choose the one that suits you best:

Method 1: use setup.py
----------------------

Inside the directory, run the following command:

..  code::

    python setup.py install

Follow the installation script, and you are done!


Method 2: build the package
---------------------------

By using this method, you will build the package from the source code and then install it. You may require to install some packages like `build <https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives>`_ if you do not have them already.

To build the package, run the following command:

..  code::

    python -m build

After the building process has finished, you will find the ``dist`` directory with different files. Go inside this directory and run the following command:

.. code::

    pip install .\neasqc-qrbs-0.4.0.tar.gz

Once the installation process is done, you have finished!