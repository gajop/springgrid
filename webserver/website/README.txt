Prerequisites:
sudo apt-get install python-dev

Installation and Setup
======================

Step-by-step install (in virtualenv):
pip install Pylons
pip install SQLAlchemy
pip install Jinja2
pip install py-bcrypt
pip install python-openid

paster setup-app development.ini

Run it
======
paster serve development.ini

# should then be available at http://127.0.0.1:5010/about

=========================================
Old instructions:
Install ``springgrid`` using easy_install::

    easy_install springgrid

Make a config file as follows::

    paster make-config springgrid config.ini

Tweak the config file as appropriate and then setup the application::

    paster setup-app config.ini

Then you are ready to go.
    paster serve development.ini

