# Copyright Hugh Perkins 2009
# hughperkins@gmail.com http://manageddreams.com
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
#  more details.
#
# You should have received a copy of the GNU General Public License along
# with this program in the file licence.txt; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-
# 1307 USA
# You can find the licence also on the web at:
# http://www.opensource.org/licenses/gpl-license.php
#
import bcrypt

"""SQLAlchemy Metadata and Session object"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, and_, schema, Table, UniqueConstraint
from sqlalchemy.orm import backref, relation

from entity import *

# SQLAlchemy session manager. Updated by model.init_model()
Session = scoped_session(sessionmaker())

account_roles = Table('role_member', Base.metadata,
   Column('role_id', Integer,ForeignKey('role.role_id'),nullable=False),
   Column('account_id', Integer,ForeignKey('account.account_id'),nullable=False),
   UniqueConstraint('role_id','account_id')
)

class Role(Base):
    __tablename__ = 'role'

    def __init__(self, role_name ):
        self.role_name = role_name

    role_id = Column(Integer,primary_key=True)
    role_name = Column(String(255), unique = True, nullable = False)

class OpenID(Base):
    __tablename__ = 'openid'

    account_id = Column(Integer, ForeignKey('account.account_id'), primary_key = True)
    openid = Column(String(255), primary_key = True)

    def __init__( self, openid ):
        self.openid = openid

class PasswordInfo(Base):
    __tablename__ = 'password'

    account_id = Column(Integer, ForeignKey('account.account_id'), primary_key = True)
    passwordsalt = Column(String(255), nullable = False)
    passwordhash = Column(String(255), nullable = False)

    def __init__(self, password):
        self.changePassword(password)

    def checkPassword(self, password):
        return bcrypt.hashpw(password, self.passwordsalt) == self.passwordhash

    def changePassword(self, newPassword):
        self.passwordsalt = bcrypt.gensalt()
        self.passwordhash = bcrypt.hashpw(newPassword, self.passwordsalt)

class Account(Base):
    __tablename__ = 'account'

    account_id = Column(Integer,primary_key=True)
    username = Column(String(255), unique = True, nullable = False)
    userfullname = Column(String(255))
    useremailaddress = Column(String(255))

    roles = relation("Role", secondary = account_roles )
    passwordinfo = relation('PasswordInfo', uselist = False)
    openids = relation('OpenID')

    def __init__(self, username, userfullname ):
        self.username = username
        self.userfullname = userfullname

    def addRole( self, role ):
        self.roles.append(role)

# simple flat config for now
class Config(Base):
    __tablename__ = 'config'

    config_key = Column(String(255),primary_key = True )
    config_value = Column(String(255), nullable = False)
    config_type = Column(String(255), nullable = False)

    # sets value of config_type appropriately, according to config_value type
    # to int, float, string or boolean
    def __init__(self, config_key, config_value ):
        self.config_key = config_key
        self.setValue( config_value )

    def setValue( self, config_value ):
        self.config_value = str(config_value)
        if type(config_value) == int:
            self.config_type = 'int'
        elif type(config_value) == float:
            self.config_type = 'float'
        elif type(config_value) == str:
            self.config_type = 'string'
        elif type(config_value) == bool:
            self.config_type = 'boolean'

    # returns config_value converted into appropriate type, according t o value of config_type
    def getValue(self):
        if self.config_type == 'int':
            return int(self.config_value)
        if self.config_type == 'float':
            return float(self.config_value)
        if self.config_type == 'string':
            return self.config_value
        if self.config_type == 'boolean':
            if self.config_value.lower() == 'true':
                return True
            return False

def addStaticData():
    import confighelper # have to import it here, otherwise Config table can't be easily
                        # imported inside confighelper, because circular import loop
    confighelper.applydefaults()

    import roles
    roles.addstaticdata()

    account = Account("admin", "admin")
    account.passwordinfo = PasswordInfo('admin')
    Session.add(account)
    account.addRole(roles.getRole('accountadmin'))
    account.addRole(roles.getRole('aiadmin'))
    account.addRole(roles.getRole('mapadmin'))
    account.addRole(roles.getRole('modadmin'))
    account.addRole(roles.getRole('leagueadmin'))
    account.addRole(roles.getRole('botrunneradmin'))
    account.addRole(roles.getRole('requestadmin'))
    Session.commit()

def createall(engine):
    Base.metadata.create_all(engine)
    openidhelper.createtables(engine)

def dropall(engine):
    Base.metadata.drop_all(engine)
    openidhelper.droptables(engine)
