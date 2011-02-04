#!/usr/bin/python

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

# manages roles

from sqlalchemy.orm import join

from utils import *
import loginhelper
import tableclasses
import sqlalchemysetup
from tableclasses import *

# list rolenames here
# they're also in the roles table, and should match
accountadmin = 'accountadmin'
aiadmin = 'aiadmin'
mapadmin = 'mapadmin'
modadmin = 'modadmin'
leagueadmin = 'leagueadmin'
botrunneradmin = 'botrunneradmin'
requestadmin = 'requestadmin'
apiclient = 'apiclient'

# note that there's probably a better way to sort out all this static data and stuff, but for
# now, this works ...

# adds any missing roles to the table, can be called as many times as you like
def addstaticdata():
   rolerows = sqlalchemysetup.session.query(Role).all()
   for rolename in [ 'accountadmin', 'aiadmin', 'mapadmin', 'modadmin', 'leagueadmin', 'botrunneradmin', 'requestadmin', 'apiclient' ]:
      rolefound = False
      for rolerow in rolerows:
         if rolerow.role_name == rolename:
            rolefound = True
      if not rolefound:
         role = Role( rolename )
         sqlalchemysetup.session.add(role)
         sqlalchemysetup.session.flush()

# returns Role object using sqlalchemy
def getRole(rolename ):
   addstaticdata()
   return sqlalchemysetup.session.query(Role).filter(Role.role_name == rolename ).first()

# returns if the logged-in user is in the named role
def isInRole(rolename):
   if not loginhelper.isLoggedOn():
      return False
   username = loginhelper.getUsername()
   return isInRole2( username, rolename )

# This is slightly easier to test, so factor it out:
def isInRole2(username, rolename):
   if rolename == None:
      print "ERROR: no rolename specified"
      return False
   if rolename == '':
      print "ERROR: no rolename specified"
      return False

   # validate rolename:
   addstaticdata()
   rolerow = sqlalchemysetup.session.query(Role).filter(Role.role_name == rolename ).first()
   if rolerow == None:
      print "ERROR: invalid rolename specified"
      return False

   account = sqlalchemysetup.session.query(Account).\
      filter(Account.username == username ).\
      filter( Account.roles.any( role_name = rolename )).first()
   return ( account != None )

# self test function
def test():
   # This supposes original static data is in the db
   if not tester.testBoolean('check if admin is accountadmin', isInRole2( 'admin', 'accountadmin'), True ):
      return
   if not tester.testBoolean('check if guest is accountadmin', isInRole2( 'guest', 'accountadmin'), False ):
      return
   print "PASS"

# running as main doesn't work for me (yet?) because the import
# doesn't work.  If someone has the solution?
if __name__ == '__main__':
   test()


