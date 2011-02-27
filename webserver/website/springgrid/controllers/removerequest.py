#!/usr/bin/python
# Copyright
# Hugh Perkins 2009
# hughperkins@gmail.com http://manageddreams.com
# Gajo Petrovic 2010
# gajop@uns.ac.rs
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

import cgitb; cgitb.enable()

import sys
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
    #currently, as MatchRequest doesn't seem to hold information on who
    #requested the match, we only allow admin to remove matches
    if not roles.isInRole(roles.accountadmin):
        jinjahelper.message("You must be logged in as an accountadmin")
        return
    [result, missingfields] = checkformvarsnotnonenotempty(['matchrequest_id'])
    if not result:
        jinjahelper.message("Please fill in all the fields.  Missing " + ",".join(missingfields) )
        return
    matchrequest_id = formhelper.getValue('matchrequest_id')
    match = sqlalchemysetup.session.query(MatchRequest).filter(MatchRequest.matchrequest_id == matchrequest_id).first()
    if match.matchrequestinprogress != None:
        jinjahelper.message("You cannot remove a match in progress")
        return
    sqlalchemysetup.session.delete(match)

    sqlalchemysetup.session.commit()

    jinjahelper.message("Removed match with id " + matchrequest_id + ".")

try:
    go()
except:
    jinjahelper.message( "An unexpected error occurred: " + str(sys.exc_info() ) )

sqlalchemysetup.close()
