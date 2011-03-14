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
from __future__ import division

import cgitb; cgitb.enable()
import os
import math
import sys

from utils import *
from core import *
from core.tableclasses import *

import core.replaycontroller as replaycontroller

sqlalchemysetup.setup()

loginhelper.processCookie()

def go():
    leaguenames = listhelper.tuplelisttolist( sqlalchemysetup.session.query( League.league_name ) )
    if len(leaguenames) == 0:
        jinjahelper.message("Please create a league first.")
        return

    leaguename = formhelper.getValue('leaguename')
    if leaguename == None:
        leaguename = leaguenames[0]
    league = leaguehelper.getLeague(leaguename)

    resultsPerPage = 100
    page = formhelper.getValue('page')
    if page == None:
        page = 1
    else:
        page = int(page)

    results = leaguehelper.getleaguematches(league)
    results = filter(lambda x: x['matchresult'][0] == True, results)
    for x in results:
        x['matchresult'] = x['matchresult'][1]
        x['botrunner_name'] = x['botrunner_name'][1]
    numPages = math.ceil(len(results) / resultsPerPage)
    results = results[(page - 1) * resultsPerPage:page * resultsPerPage]

    jinjahelper.rendertemplate( 'viewresults.html', results = results, leaguenames = leaguenames, league = league, springgridurl = confighelper.getValue('springgridwebsite' ), page = page, numPages = numPages )

go()

sqlalchemysetup.close()
