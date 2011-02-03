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
import sys
import math

from utils import *
from core import *
from core.tableclasses import *

import core.replaycontroller as replaycontroller

sqlalchemysetup.setup()

loginhelper.processCookie()

def go():
   resultsPerPage = 100
   page = formhelper.getValue('page')
   if page == None:
      page = 1
   else:
      page = int(page)
   requests = sqlalchemysetup.session.query(MatchRequest).filter(MatchRequest.matchresult != None )
   numPages = int(math.ceil(requests.count() / resultsPerPage))
   requests = requests[(page - 1) * resultsPerPage:page * resultsPerPage]
   replaypathbyrequest = {}
   infologpathbyrequest =  {}
   for request in requests:
      replaypath = replaycontroller.getReplayPath(request.matchrequest_id)
      if os.path.isfile( replaypath ):
         replaypathbyrequest[request] = replaycontroller.getReplayWebRelativePath( request.matchrequest_id)
      if os.path.isfile( replaycontroller.getInfologPath( request.matchrequest_id) ):
         infologpathbyrequest[request] = replaycontroller.getInfologWebRelativePath( request.matchrequest_id)

   jinjahelper.rendertemplate( 'viewresults.html', requests = requests, replaypathbyrequest = replaypathbyrequest, infologpathbyrequest = infologpathbyrequest, numPages = numPages, page = page)

try:
   go()
except:
   jinjahelper.message("Something went wrong. " + str(sys.exc_value))

sqlalchemysetup.close()

