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

from tableclasses import *
import sqlalchemysetup
import leaguehelper
import aihelper
import matchrequestcontroller_gridclient

# does for one league
def schedulematchesforleague( league, matchrequestqueue, matchresults ):
    ais = leaguehelper.getleagueais( league )
    indextoai = getindextoai(league)
    aiqueuedpairmatchcount = getaipairmatchcount(matchrequestqueue, league, ais, indextoai )
    aifinishedpairmatchcount = getaipairmatchcount(matchresults, league, ais, indextoai )
    aipairs = []
    playagainstself = league.playagainstself
    sides = [int(i) for i in league.sides.split("vs")]
    for outeraiindex in xrange(len(ais)):
        for inneraiindex in xrange(len(ais)):
            if not playagainstself and outeraiindex == inneraiindex:
                continue
            totalrequestcount = aiqueuedpairmatchcount[outeraiindex][inneraiindex] + aifinishedpairmatchcount[outeraiindex][inneraiindex]
            if totalrequestcount < league.nummatchesperaipair * len(sides):
                if len(sides) == 2:
                    first = sides[0]
                    second = sides[1]
                    for i in xrange( league.nummatchesperaipair - totalrequestcount ):
                        aipairs.append([{"ai_name":indextoai[outeraiindex].ai_name, "ai_version":indextoai[outeraiindex].ai_version, "ai_side":first}, {"ai_name":indextoai[inneraiindex].ai_name, "ai_version":indextoai[inneraiindex].ai_version, "ai_side":second}])
                    for i in xrange( league.nummatchesperaipair - totalrequestcount ):
                        aipairs.append([{"ai_name":indextoai[outeraiindex].ai_name, "ai_version":indextoai[outeraiindex].ai_version, "ai_side":second}, {"ai_name":indextoai[inneraiindex].ai_name, "ai_version":indextoai[inneraiindex].ai_version, "ai_side":first}])
                else:
                    side = sides[0]
                    for i in xrange( league.nummatchesperaipair - totalrequestcount ):
                        aipairs.append([{"ai_name":indextoai[outeraiindex].ai_name, "ai_version":indextoai[outeraiindex].ai_version, "ai_side":side}, {"ai_name":indextoai[inneraiindex].ai_name, "ai_version":indextoai[inneraiindex].ai_version, "ai_side":side}])
                    #scheduleleaguematch( league, indextoai[outeraiindex], indextoai[inneraiindex] )
                aiqueuedpairmatchcount[outeraiindex][inneraiindex] = league.nummatchesperaipair - aifinishedpairmatchcount[outeraiindex][inneraiindex]
                aiqueuedpairmatchcount[inneraiindex][outeraiindex] = league.nummatchesperaipair - aifinishedpairmatchcount[outeraiindex][inneraiindex]
    scheduleleaguematches(league, aipairs)

def scheduleleaguematch( league, ai0, ai1 ):
    matchrequest_id = matchrequestcontroller_gridclient.addmatchrequest( ai0 = ai0, ai1 = ai1, map_name = league.map_name, mod_name = league.mod_name, speed = league.speed, softtimeout = league.softtimeout, hardtimeout = league.hardtimeout )
    leagueMatch = LeagueMatch(matchrequest_id, league.league_id)
    sqlalchemysetup.session.add(leagueMatch)
    sqlalchemysetup.session.commit()

def scheduleleaguematches(league, aipairs):
    matches = []
    for aipair in aipairs:
        match = {}
        match["map_name"] = league.map_name
        match["mod_name"] = league.mod_name
        match["ais"] = aipair
        match["softtimeout"] = league.softtimeout
        match["hardtimeout"] = league.hardtimeout
        match["speed"] = league.speed
        match["options"] = []
        matches.append(match)
    matchrequest_ids = matchrequestcontroller_gridclient.addmatchrequests(matches)
    leaguematches = [LeagueMatch(matchrequest_id, league.league_id) for matchrequest_id in matchrequest_ids]
    sqlalchemysetup.session.add_all(leaguematches)
    sqlalchemysetup.session.commit()


# returns [ dict from ai to zero-based aiindex, dict from index to ai ]
# only returns ais that match the league, ie have at least the same options as league
def getindextoai(league ):
    # assume this query is cached in memory, so fine to redo
    #aitoindex = {}  # dict from ai to aiindex
    indextoai = {} # dict from index to ai
    ais = leaguehelper.getleagueais( league )
    for ai in ais:
        indextoai[ len(indextoai) ] = ai
    #return [ aitoindex, indextoai ]
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
