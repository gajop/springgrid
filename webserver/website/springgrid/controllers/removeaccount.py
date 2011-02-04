#!/usr/bin/python

# Copyright Hugh Perkins 2009
# hughperkins@gmail.com http://manageddreams.com
#
# This program is free software; you can redistribute it and/or aiify it
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

# lets a user add a single account to the database

import cgitb; cgitb.enable()
import cgi

from utils import *
from core import *
from core.tableclasses import *

sqlalchemysetup.setup()

loginhelper.processCookie()

if not roles.isInRole(roles.accountadmin):
   jinjahelper.message( "You must be logged in as an accountadmin" )
else:
   username = formhelper.getValue('username')

   if username != None and username != '':
      if roles.isInRole2( username, roles.accountadmin ):
         jinjahelper.message( "Please drop the accountadmin role from " + username + " and try again" )
      else:
         account = sqlalchemysetup.session.query( Account ).filter( Account.username == username ).first()
         if account.passwordinfo != None:
            sqlalchemysetup.session.delete( account.passwordinfo )
         for openid in account.openids:
            sqlalchemysetup.session.delete( openid )
         sqlalchemysetup.session.delete( account )
         jinjahelper.message( "Removed ok" )
   else:
      jinjahelper.message( "Please fill in the fields and try again" )

sqlalchemysetup.close()

