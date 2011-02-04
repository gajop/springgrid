# Copyright Hugh Perkins 2004, 2009
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

# functions for login, cookies etc...

import Cookie
import random
import cgi
import string
import os
import os.path
import md5

from sqlalchemy.orm import join

from utils import *

import sqlalchemysetup
import tableclasses
# from tableclasses import *

gusername = ""  # first call loginhelper.processCookie().  If the user
                # is already logged in after that, then gusername will no
                # longer be blank
                # testing gusername != '' is sufficient to check if the user
                # is logged in
loginhtml = ""
cookiereference = ''
cookie = Cookie.SimpleCookie()

saltlength = 200

def GenerateRef():
   return stringhelper.getRandomAlphaNumericString(40)

def hasPassword():
   account = sqlalchemysetup.session.query(tableclasses.Account).filter( tableclasses.Account.username == gusername ).first()
   if account == None:
      return False
   if account.passwordinfo == None:
      return False
   return True
   
def isLoggedOn():
   global gusername
   return ( gusername != '')

def getUsername():
   global gusername
   return gusername

# returns a salt string
def createSalt():
   global saltlength
   return stringhelper.getRandomPrintableString(saltlength)

# returns True if password correct, otherwise false
def validateUsernamePassword( username, password ):
   global authmethod

   account = sqlalchemysetup.session.query(tableclasses.Account).filter( tableclasses.Account.username == username ).first()
   if account == None:
      return False
   if account.passwordinfo == None:
      return False
   result = account.passwordinfo.checkPassword( password )
   return result

def logonUserWithAuthenticatedOpenID( openidurl ):
   global gusername
   global loginhtml
   global cookie
   global cookiereference
   global authmethod

   cookiereference = GenerateRef()

   cookie = Cookie.SimpleCookie()
   cookie["cookiereference"] = cookiereference

   account = None
   # note: this could be optimized a little...
   for thisaccount in sqlalchemysetup.session.query(tableclasses.Account):
      for openid in thisaccount.openids:
         if openid.openid == openidurl:
            account = thisaccount
   if account == None:
      # create new account
      account = tableclasses.Account(openidurl, openidurl )
      account.openids.append( tableclasses.OpenID( openidurl ) )
      sqlalchemysetup.session.add( account )

   cookierow = tableclasses.Cookie( cookiereference, account )
   sqlalchemysetup.session.add(cookierow)
   sqlalchemysetup.session.commit()

   gusername = account.username
   loginhtml = "<p>Logged in as: " + gusername + "</p>"

def logonUserWithPassword(username, password):
   global gusername
   global loginhtml
   global cookie
   global cookiereference

   gusername = ""
   if not validateUsernamePassword( username, password ):
      loginhtml =  "<h4>Logon error: Please check your username and password.</h4>"
      return

   cookiereference = GenerateRef()

   cookie = Cookie.SimpleCookie()
   cookie["cookiereference"] = cookiereference

   accountrow = sqlalchemysetup.session.query(tableclasses.Account).filter(tableclasses.Account.username == username ).first()
   if accountrow == None:
      loginhtml =  "<h4>Logon error: Please check your username and password.</h4>"
      return 

   cookierow = tableclasses.Cookie( cookiereference, accountrow )
   sqlalchemysetup.session.add(cookierow)
   sqlalchemysetup.session.commit()

   gusername = username
   loginhtml = "<p>Logged in as: " + gusername + "</p>"

def changePassword( username, password ):
   account = sqlalchemysetup.session.query(tableclasses.Account).filter( tableclasses.Account.username == username ).first()
   account.passwordinfo.changePassword( password )
   sqlalchemysetup.session.commit()
   return True

# can use commandline arguments to login, or just use querystring
# if there is a cookie, uses that
def processCookie():
   global cookie, cookiereference, gusername, loginhtml

   gusername = ''
   cookie = Cookie.SimpleCookie( os.environ.get("HTTP_COOKIE"))
   c = cookie.output( "Cookie: " )
   if(not c):
      # check query string, and if username and password are ok, set gusername from that
      if formhelper.getValue('username') != '' and formhelper.getValue('password') != '':
         if validateUsernamePassword( formhelper.getValue('username'), formhelper.getValue('password') ):
            gusername = formhelper.getValue('username')
      return    

   if not cookie.has_key( "cookiereference" ):
      return

   cookiereference = str( cookie["cookiereference"].value )

   cookierow = sqlalchemysetup.session.query(tableclasses.Cookie).filter(tableclasses.Cookie.cookiereference == cookiereference ).first()
   if cookierow == None:
      return

   # Note: could consider migrating from username string to account object
   gusername = cookierow.account.username

   if gusername == '':
      return

   loginhtml = "<p>Logged in as: " + gusername + "</p>"

def logoutUser():
   global cookie, cookiereference, gusername, loginhtml
   
   cookierow = sqlalchemysetup.session.query(tableclasses.Cookie).filter(tableclasses.Cookie.cookiereference == cookiereference ).first()
   if cookierow != None:
      sqlalchemysetup.session.delete(cookierow)
      sqlalchemysetup.session.commit()
   
   cookiereference = '0'
   cookie = Cookie.SimpleCookie()
   gusername = ""
   loginhtml = ""



