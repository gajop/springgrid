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

# The job of this module is to schedule matches for the various leagues.

# For now, initial first implementation, we will do the following:
# - for each league, take all ais
# - pair up
# - for each pair, check that the matchrequest table contains at least nummatchesperaipair
#   matches
# - otherwise schedule new ones

#from tableclasses import *
#import sqlalchemysetup
#import leaguehelper
#import aihelper
#import matchrequestcontroller_gridclient

from springgrid.lib.base import Session
from springgrid.model.meta import League, LeagueAI, AI, MatchRequest, Map, Mod, ModSide

# does for one league
def schedulematchesforleague(league, matchrequestqueue, matchresults):
    ais = Session.query(AI).join(LeagueAI).filter(LeagueAI.league_id ==\
                league.league_id).all()
                
    map_name = Session.query(Map).filter(Map.map_id == league.map_id).first()
    mod_name = Session.query(Mod).filter(Mod.mod_id == league.mod_id).first()
               
    indextoai = getindextoai(ais)
    aiqueuedpairmatchcount = getaipairmatchcount(matchrequestqueue, league, ais, indextoai)
    aifinishedpairmatchcount = getaipairmatchcount(matchresults, league, ais, indextoai)
    aipairs = []
    playagainstself = league.playagainstself
    sides = [int(i) for i in league.sides.split("vs")]
    
    matchrequests = []    
    for outeraiindex in xrange(len(ais)):
        for inneraiindex in xrange(len(ais)):
            if not playagainstself and outeraiindex == inneraiindex:
                continue
            totalrequestcount = aiqueuedpairmatchcount[outeraiindex][inneraiindex] + aifinishedpairmatchcount[outeraiindex][inneraiindex]
            if totalrequestcount < league.nummatchesperaipair * len(sides):
                if len(sides) == 2:
                    first = Session.query(ModSide).filter(ModSide.mod_side_id == sides[0]).first()
                    second = Session.query(ModSide).filter(ModSide.mod_side_id == sides[1]).first()
                    
                    for i in xrange( league.nummatchesperaipair - totalrequestcount ):
                        matchrequest = MatchRequest( indextoai[outeraiindex], indextoai[inneraiindex], map_name, mod_name,\
                            league.speed, league.softtimeout, league.hardtimeout,\
                            first, second, league.league_id)
                        matchrequests.append(matchrequest)                        
                    for i in xrange( league.nummatchesperaipair - totalrequestcount ):
                        
                    
                        matchrequest = MatchRequest( indextoai[outeraiindex], indextoai[inneraiindex], map_name, mod_name,\
                            league.speed, league.softtimeout, league.hardtimeout,\
                            second, first, league.league_id)
                        matchrequests.append(matchrequest)  
                else:
                    side = Session.query(ModSide).filter(ModSide.mod_side_id == sides[0]).first()
                    for i in xrange( league.nummatchesperaipair - totalrequestcount ):
                        matchrequest = MatchRequest( indextoai[outeraiindex], indextoai[inneraiindex], map_name, mod_name,\
                            league.speed, league.softtimeout, league.hardtimeout,\
                            side, side, league.league_id)
                        matchrequests.append(matchrequest) 
                aiqueuedpairmatchcount[outeraiindex][inneraiindex] = league.nummatchesperaipair - aifinishedpairmatchcount[outeraiindex][inneraiindex]
                aiqueuedpairmatchcount[inneraiindex][outeraiindex] = league.nummatchesperaipair - aifinishedpairmatchcount[outeraiindex][inneraiindex]
    
    #save all matches to the database
    Session.add_all(matchrequests)
    Session.commit()


# returns [ dict from ai to zero-based aiindex, dict from index to ai ]
# only returns ais that match the league, ie have at least the same options as league
def getindextoai(ais):
    # assume this query is cached in memory, so fine to redo
    #aitoindex = {}  # dict from ai to aiindex
    indextoai = {} # dict from index to ai
    for ai in ais:
        indextoai[ len(indextoai) ] = ai
    return indextoai

# return 2d list ([][]), indexed by indexes returned by getaiindexes
# showing the numer of matches in the queue between each pair of ais
# have to pass in requests one wants to consider
# that means one can pass in all requests, or just finished, or just not finished
# etc...
def getaipairmatchcount(requests, league, ais, indextoai ):
    # go through each matchrequest in the queue, and increment matchcountarray member
    # we go through all requests that match the league: both the ones that have results, and the ones
    # that don't
    matchcountarray = []  # 2d array of count of matches from one ai to another
    # build up empty array
    for outeraiindex in xrange(len(ais)):
        thisline = []
        matchcountarray.append(thisline)
        for inneraiindex in xrange(len(ais)):
            thisline.append(0)
    for matchrequest in requests:
        if matchrequest['map_name'] != league.map_name:
            continue
        if matchrequest['mod_name'] != league.mod_name:
            continue
        ai0index = getindex( indextoai, matchrequest['ais'][0] )
        ai1index = getindex( indextoai, matchrequest['ais'][1] )
        # add both ways around
        matchcountarray[ai0index][ai1index] = matchcountarray[ai0index][ai1index] + 1
        if ai0index != ai1index:
            matchcountarray[ai1index][ai0index] = matchcountarray[ai1index][ai0index] + 1
    return matchcountarray

# ideally, we should index from ai to index, but you can't hash dicts... need to rethink that
def getindex( indextoai, ai ):
    for index in indextoai.keys():
        if indextoai[index].ai_name == ai['ai_name'] and indextoai[index].ai_version == ai['ai_version']:
            return index
    return None

# does for all leagues
def schedulematches():
    for league in sqlalchemysetup.session.query(League):
        schedulematchesforleague(league )
