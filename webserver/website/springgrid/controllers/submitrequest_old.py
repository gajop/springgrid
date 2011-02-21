#!/home/gajop/radni_direktorijum/env_springgrid/bin/python

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

# This is basically used for debug
# It pumps a single request into the queue
# Once there are other systems in place, this file will either be purged, moved
# elsewhere, or protected by some admin authentication system
# for now, no authentication...

# also, no form for now, we just put the request into the querystring ;-)

import cgitb; cgitb.enable()
import sys
import os
import Cookie
# import cookiefile
import cgi

import config

from utils import *
from core import *
from core.tableclasses import *

sqlalchemysetup.setup()

loginhelper.processCookie()

def checkformvarsnotnonenotempty( vars ):
   failed = []
   for var in vars:
      if formhelper.getValue(var) == None or formhelper.getValue(var) == '':
         failed.append(var)
   return [ len(failed) == 0, failed ]

def go():
   if not loginhelper.isLoggedOn():
      jinjahelper.message( "Please login first." )
      return

   [result, missingfields ] = checkformvarsnotnonenotempty(['ai0nameversion', 'ai1nameversion', 'ai0side', 'ai1side', 'mapname', 'modname', 'speed', 'softtimeout', 'hardtimeout'])
   if not result:
      jinjahelper.message("Please fill in all the fields.  Missing " + ",".join(missingfields) )
      return

   ai0nameversion = formhelper.getValue("ai0nameversion")
   ai0name = ai0nameversion.split("|")[0]
   ai0version = ai0nameversion.split("|")[1]
   ai0side = int(formhelper.getValue("ai0side"))
   ai1nameversion = formhelper.getValue("ai1nameversion")
   ai1name = ai1nameversion.split("|")[0]
   ai1version = ai1nameversion.split("|")[1]
   ai1side = int(formhelper.getValue("ai1side"))
   mapname = formhelper.getValue("mapname")
   modname = formhelper.getValue("modname")
   speed = formhelper.getValue("speed")
   softtimeout = formhelper.getValue("softtimeout")
   hardtimeout = formhelper.getValue("hardtimeout")

   #if matchrequestcontroller.submitrequest( matchrequest ):
    #  jinjahelper.message( "Submitted"
      # could be nice to print out queue here, or make another page for that

   map = sqlalchemysetup.session.query(Map).filter(Map.map_name == mapname ).first()
   mod = sqlalchemysetup.session.query(Mod).filter(Mod.mod_name == modname ).first()
   ai0 = sqlalchemysetup.session.query(AI).filter(AI.ai_name == ai0name ).filter(AI.ai_version == ai0version ).first()
   ai1 = sqlalchemysetup.session.query(AI).filter(AI.ai_name == ai1name ).filter(AI.ai_version == ai1version ).first()
   ai0side = sqlalchemysetup.session.query(ModSide).filter(ModSide.mod_side_id == ai0side).first()
   ai1side = sqlalchemysetup.session.query(ModSide).filter(ModSide.mod_side_id == ai1side).first()

   matchrequest = MatchRequest( ai0 = ai0, ai1 = ai1, map = map, mod = mod, speed = speed, softtimeout = softtimeout, hardtimeout = hardtimeout, ai0_side=ai0side, ai1_side=ai1side)

   # add options:
   availableoptions = sqlalchemysetup.session.query(AIOption)
   # get selected options from form submission:
   for option in availableoptions:
      if formhelper.getValue( "option_" + option.option_name ) != None:
         matchrequest.options.append( option )
   sqlalchemysetup.session.add( matchrequest )
   
   sqlalchemysetup.session.commit()

   jinjahelper.message( "Submitted ok." )

go()

sqlalchemysetup.close()

