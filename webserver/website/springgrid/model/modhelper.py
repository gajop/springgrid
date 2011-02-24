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

import sys

from springgrid.lib.base import Session
from meta import Mod, ModSide
import botrunnerhelper


# returns True if exists, or added ok, otherwise False
def addmodifdoesntexist(modname, modarchivechecksum, sidenames):
   mod = Session.query(Mod).filter(Mod.mod_name == modname ).first()
   if mod == None:
      try:
         mod = Mod( modname )
         mod.mod_archivechecksum = modarchivechecksum
         Session.add(mod)
         Session.commit()
         Session.flush()
         mod = Session.query(Mod).filter(Mod.mod_name == modname ).first()
         sides = [ModSide(sidename, mod.mod_id) for sidename in sidenames]
         Session.add_all(sides)
         Session.commit()
      except:
         return(False, "error adding to db: " + str( sys.exc_value ) )

      return (True,'')

   if mod.mod_name != modname:
      mod.mod_name = modname
      Session.flush()

   if mod.mod_archivechecksum == None:
      mod.mod_archivechecksum = modarchivechecksum
      try:
         Session.commit()
         return (True,'')          
      except:
         return(False, "error updating db: " + str( sys.exc_value ) )
 
   if mod.mod_archivechecksum != modarchivechecksum:
      return (False,"mod archive checksum doesn't match the one already on the website.")

   return (True,'')

def getMod( modname ):
   return Session.query(Mod).filter(Mod.mod_name == modname ).first()

# return list of supported modnames
def getsupportedmods( botrunnername ):
   botrunner = botrunnerhelper.getBotRunner( botrunnername )
   if botrunner == None:
      return []
   if botrunner.supportedmods == None:
      return []
   supportedmodnames = []
   for mod in botrunner.supportedmods:
      supportedmodnames.append(mod.mod_name)
   return supportedmodnames

def setbotrunnersupportsthismod( botrunnername, modname ):
   # Now, register the mod as supported mod
   botrunner = botrunnerhelper.getBotRunner( botrunnername )
   for mod in botrunner.supportedmods:
      if mod.mod_name == modname:
       return (True,'')
   mod = getMod(modname)
   botrunner.supportedmods.append(mod)
   Session.commit()
   return (True,'')

