Prerequisites:
sudo apt-get install python-dev

Installation and Setup
======================

Step-by-step install (in virtualenv):
pip Pylons
pip SQLAlchemy
pip Jinja2
pip py-bcrypt
pip python-openid

paster setup-app development.ini

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

