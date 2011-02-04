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

import cgi
import datetime

from utils import *
import sqlalchemysetup
import tableclasses
import confighelper
from tableclasses import *

botrunnername = ""

def botrunnerauthorized():
   global botrunnername 

   botrunnername = formhelper.getValue("botrunnername")
   sharedsecret = formhelper.getValue("sharedsecret")
   return validatesharedsecret( botrunnername, sharedsecret )

def getBotRunner(botrunnername ):
   return sqlalchemysetup.session.query(BotRunner).filter(tableclasses.BotRunner.botrunner_name == botrunnername ).first()

def getBotRunnerSession(botrunnername, botrunner_session_id ):
   botrunner = getBotRunner( botrunnername )
   if botrunner == None:
      return None
   for session in botrunner.sessions:
      if session.botrunner_session_id == botrunner_session_id:
         return session
   return None

def expireBotRunnerSession( botrunner, session ):
   # first, remove any matchrequests in progress attached to this session
   requestsinprogress = sqlalchemysetup.session.query(MatchRequest).filter(MatchRequest.matchresult == None).filter(MatchRequest.matchrequestinprogress != None)
   for request in requestsinprogress:
      if request.matchrequestinprogress.botrunner == botrunner and request.matchrequestinprogress.botrunnersession == session:
         sqlalchemysetup.session.delete( request.matchrequestinprogress )
   sqlalchemysetup.session.delete( session )

   # then, delete session
   sqlalchemysetup.session.delete( session )

def purgeExpiredSessions():
   botrunners = sqlalchemysetup.session.query(BotRunner)
   for botrunner in botrunners:
      for session in botrunner.sessions:
         lastpingtime =  session.lastpingtime
         if lastpingtime != None:
            lastpingtimedate = dates.dateStringToDateTime( lastpingtime )
            secondssincelastping = dates.timedifftototalseconds( datetime.datetime.now() - lastpingtimedate )
            if secondssincelastping > confighelper.getValue('expiresessionminutes') * 60:
               expireBotRunnerSession( botrunner, session )

def validatesharedsecret(lbotrunnername, sharedsecret):
   global botrunnername

   botrunner = getBotRunner( lbotrunnername )

   if botrunner == None: 
      # Never seen this botrunner before, just add it
      botrunner = BotRunner( lbotrunnername, sharedsecret )
      sqlalchemysetup.session.add(botrunner)
      sqlalchemysetup.session.commit()

      # if this fails, return true anyway
      return True
   else:
      if botrunner.botrunner_sharedsecret == sharedsecret:
         botrunnername = lbotrunnername
         return True
      return False

def getOwnerUsername(botrunnername):
   botrunner = getBotRunner( botrunnername )
   if botrunner == None:
      return None
   if botrunner.owneraccount == None:
      return None
   return botrunner.owneraccount.username

