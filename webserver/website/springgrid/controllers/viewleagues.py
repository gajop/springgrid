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

import cgitb; cgitb.enable()

from utils import *
from core import *
from core.tableclasses import *

sqlalchemysetup.setup()

loginhelper.processCookie()

leagues = sqlalchemysetup.session.query(League)

showform = loginhelper.gusername != ''

maps = gridclienthelper.getproxy().getmaps()
mods = gridclienthelper.getproxy().getmods()
sides = gridclienthelper.getproxy().getmodsides()
ais = gridclienthelper.getproxy().getais()
modsides = {}
for i, mod in enumerate(mods):
    modsides[mod] = (i, [])
for side in sides:
    modsides[side["mod_name"]][1].append((side["mod_side_name"], side["mod_side_id"]))
sides = modsides
speeds = [20] #default
speeds.extend(range(1, 10))
speeds.extend(range(10, 101, 5))
timeouts = speeds
tmpais = {}
for ai in ais:
    tmpais[ai["ai_id"]] = ai["ai_name"] + " " + ai["ai_version"]

sidemodes = { "allsame" : "All same", "xvsy" : "X vs Y" }

jinjahelper.rendertemplate('viewleagues.html', leagues = leagues, showform = showform, maps = maps, mods = mods, speeds = speeds, timeouts = timeouts, sidemodes = sidemodes, sides = sides, ais = tmpais)

sqlalchemysetup.close()
