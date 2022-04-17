Prerequisites :

1. Pycharm
2. MongoDB and Mongo Compass

1. Download the zipped folder named C01-Project-A-Assessment-Weather-Data.zip,
unzip it on your local machine, and save it. Go into the directory named
C01-Project-A-Assessment-Weather-Data.
2. Make sure you have Python 3.6 or higher installed. At your command prompt, run:
$ python --version
Python 3.7.3
If not installed, install the latest available version of Python 3.
3. Please install MongoDB and MongoDB Compass. Please see
docs/MongoDB-Install for instructions on the download location and setup.
4. Install pymongo and bson python modules. Please see
docs/C01-Project-A-MongoDB-Prep-Material.ipynb for help in installing modules
5. Modify the connection parameters in src/Database.py if needed, for your setup.
6. Go to the src folder, and run setup.py to create the database, collections and to
populate data in them, using config/users.csv and config/devices.csv. Please note
that this clears the database and adds everything again whenever you run it.
$ python3 setup.py (On many Linux platforms)
OR
$ python setup.py (On Windows platforms)
In any case, one of these two commands should work.
7. You can now examine and run main.py. This will currently run various simple calls
that show how to use the various models. As you solve the problems, you’ll be
frequently modifying and running this file. You can comment or modify the initial code
as needed.
8. Alternatively, you could install a popular Python IDE, such as PyCharm or Visual
Studio Code, and select a command to build the project from there.
9. Once the program is ready to submit, zip the parent folder
C01-Project-A-Assessment-Weather-Data, and upload the new zip file as
C01-Project-A-Assessment-Weather-Data.zip.It is now ready for evaluation
