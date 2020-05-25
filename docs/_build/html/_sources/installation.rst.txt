Installation and Deployment
***************************
There are a number of dependencies that must be installed on to the Raspberry Pis
before deployment. This has been broken up into two device types - a Master Pi and
an Agent Pi. While it is possible to install all dependencies on all devices, it is 
ill-advised to import all the modules as there are significant overhead costs associated.

Source files should be downloaded and data structures maintained.

These instructions presume each instance is deployed on a unique device. If 
running simultaneously on the same device, consider using a virtual environment.

::
    sudo apt install python3-venv
    pip3 install virtualenv 

    cd ~/webapp 
    python3 -m venv venv 
    source venv/bin/activate

Agent Pi Installation
=====================
The Agent requires a large number of dependencies due to the face recognition requirements.
Different environments may affect these instructions. 

Importantly it uses the dateutil package to parse dates. If this is deployed on Python 3.7 or
newer this can be deprecated and internal datetime functions used instead.

The following is adapted from a guide provided by RMIT University in the course 
Programming Internet of Things Semester 1 2020, which is in turn adapted from 
https://www.pyimagesearch.com/2017/10/09/optimizing-opencv-on-the-raspberry-pi/ 
and https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

.. note:: This installation can be quite time consuming. 1-3 hours depending on the hardware.

.. warning:: These instructions modify the CONF_SWAPSIZE which is highly dependent on 
    the storage device employed. Your installation is not guaranteed without these changes. You can 
    ignore all but the first and last changes to the containing file if you are installing in one 
    sesssion.

In a terminal: ::

    pip install python-dateutil

    sudo apt-get purge wolfram-engine
    sudo apt-get purge libreoffice*
    sudo apt-get clean
    sudo apt-get autoremove

    sudo apt-get update && sudo apt-get upgrade

    sudo apt-get install build-essential cmake pkg-config
    sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
    sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
    sudo apt-get install libxvidcore-dev libx264-dev
    sudo apt-get install libgtk2.0-dev libgtk-3-dev
    sudo apt-get install libcanberra-gtk*
    sudo apt-get install libatlas-base-dev gfortran
    sudo apt-get install python2.7-dev python3-dev

    cd ~
    wget -O opencv.zip https://github.com/opencv/opencv/archive/3.3.0.zip
    unzip opencv.zip
    wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.3.0.zip
    unzip opencv_contrib.zip

    pip3 install numpy

    cd ~/opencv-3.3.0/
    mkdir build
    cd build
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.3.0/modules \
        -D ENABLE_NEON=ON \
        -D ENABLE_VFPV3=ON \
        -D BUILD_TESTS=OFF \
        -D INSTALL_PYTHON_EXAMPLES=OFF \
        -D BUILD_EXAMPLES=OFF ..

Update CONF_SWAPSIZE to a larger size: ::

    sudo nano /etc/dphys-swapfile

    # Set size to an absolute value, leaving empty (default) then uses computed value
    # You may not wish to use this, unless you have a special disk situation
    # CONF_SWAPSIZE=100
    CONF_SWAPSIZE=1024

    sudo /etc/init.d/dphys-swapfile restart

Continue installing cv2: ::

    make -j4

    sudo make install
    sudo ldconfig

    cd /usr/local/lib/python3.5/dist-packages/

    sudo mv cv2.cpython-35m-arm-linux-gnueabihf.so cv2.so

    cd ~

Test OpenCV: ::

    python3

    >>> import cv2
    >>> cv2.__version__
    '3.3.0'
    >>> quit()

Install dlib and face_recognition python3 packages: ::

    sudo apt-get install build-essential \
        cmake \
        gfortran \
        git \
        wget \
        curl \
        graphicsmagick \
        libgraphicsmagick1-dev \
        libatlas-dev \
        libavcodec-dev \
        libavformat-dev \
        libboost-all-dev \
        libgtk2.0-dev \
        libjpeg-dev \
        liblapack-dev \
        libswscale-dev \
        pkg-config \
        python3-dev \
        python3-numpy \
        python3-pip \
        zip

    sudo apt-get install python3-picamera

    pip3 install --upgrade picamera[array]

    pip3 install dlib
    pip3 install face_recognition

Reset CONF_SWAPSIZE to a smaller size: ::

    sudo nano /etc/dphys-swapfile

    CONF_SWAPSIZE=100
    # CONF_SWAPSIZE=1024

    sudo /etc/init.d/dphys-swapfile restart

Instal imutils python3 package: ::

    pip3 install imutils


Master Pi Installation
======================

The dependencies that must be installed are as follows, presuming you are operating in
a UNIX environment though you may need to alter these to ensure you succesfully install
all modules. ::

    pip install flask

It may be necessary to set your Flask environment variable before executing.
For example: ::

    export FLASK_APP=website.py

Then execute with to test: ::

    flask run

If you do not wish to set your environment variable each time i.e., in a virtual
environment, use the python-dotenv package. ::

    pip install python-dotenv

Install the database dependencies. ::

    sudo apt install default-libmysqlclient-dev  
    sudo apt install mysql-client # this might not work 
    pip3 install mysqlclient 

Then create a .flaskenv file at the project's top level directory with the 
following (this file may exist): ::

    FLASK_APP=website.py

Forms validation is assisted by the WTForms package. ::

    pip install -U WTForms

Email validatioon with WTForms requires an additional external dependency: ::

    pip3 install email-validator

Integration of forms into flask is handled by Flask-WTF. ::

    pip install flask-wtf

SQLAlchemy has been used for database integration. Install Flask-SQLAlchemy
to integrate it with Flask: ::

    pip install -U Flask-SQLAlchemy

It is also necessary to cater for situations where the database is being migrated. 
This is additionally useful for creating a new database if none exists.
To assist with this install Flask-Migrate which uses Alembic: ::

    pip install Flask-Migrate

The commands to use Flask-Migrate are accessed with the flask command. 
Create a migration repository (will generate a migrations folder if one
does not exist). 

.. note:: At release, "<table name>" is called "second create".

::

    flask db init
    flask db migrate -m "<table name>"

It is important to ensure that the new database conforms to requirements - 
confirm this before proceding with the upgrade if migrating from an 
existing database. ::

    flask db upgrade

Optional: It is possible to seed the database with test data in a python shell, but due to the
complexity of the model, it is not recommended to do this but if errors are
made, these can be rolled back. The <table names> and <object> is specific to 
the database implementation. ::

    from app import db
    from app.models import <table names>
    db.session.add(<object>)
    db.session.commit()
    db.session.rollback()

Encryption is assisted with the Werkzeug library. ::

    pip install -U Werkzeug

And user login and persistence in the session is achieved with
the Flask-Login library: ::

    pip install Flask-Login



Agent Pi Deployment
===================

Simply run the :mod:`agentpi` python module from the AgentPi directory. ::
    
    python3 agentpi.py


Master Pi Deployment
====================
To deploy the API and database, run the following command in the carapi 
directory, where IP_ADDRESS is the address you want to host the apifrom, 
and PORT is the relevant port. ::

    flask run --host IP_ADDRESS --port PORT


To deploy the website, run the following command in the website directory,
where IP_ADDRESS is the address you want to host the website on. ::

    flask run --host IP_ADDRESS

It is not necessar to host the socket server with the database, and as such,
it is neccessary to set the address in :mod:`masterpiresponder`, as is the 
address of the hosting IP in the :mod:`socketresponder`. These are expected
to remain relatively static upon securing of a domain.
Once compelte simply run the following command in the AgentPi directory. ::

    python3 socketresponder.py