# Copyright Hugh Perkins 2009
# Copyright Gajo Petrovic 2011
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

from springgrid.lib.base import Session
from springgrid.model.meta import League, LeagueAI, LeagueMap, AI, MatchRequest, Map, Mod, ModSide
import random

# does for one league WARNING: should be used when creating a league, does not commit to DB
def addLeagueMatches(league, matchRequestQueue, matchResults):
    ais = Session.query(AI).join(LeagueAI).filter(LeagueAI.league_id ==\
                league.league_id).all()
    maps = Session.query(Map).join(LeagueMap).filter(LeagueMap.league_id ==\
                league.league_id).all()
    mod = Session.query(Mod).filter(Mod.mod_id == league.mod_id).first()

    playAgainstSelf = league.play_against_self
    if league.side_modes == "xvsy":
        sides = [int(i) for i in league.sides.split("vs")]
    else:
        sides = [int(league.sides)]
    
    matchRequests = []    
    for i, ai0 in enumerate(ais[:-1]):
        for j, ai1 in enumerate(ais[i:]):
            if not playAgainstSelf and ai0.ai_id == ai1.ai_id:
                continue
            first = Session.query(ModSide).filter(ModSide.mod_side_id == sides[0]).first()
            if len(sides) == 2:
                second = Session.query(ModSide).filter(ModSide.mod_side_id == sides[1]).first()
                allSides = [(first, second), (second, first)]
            else:
                allSides = [(first, first)]
            for firstSide, secondSide in allSides:
                pickedMaps = {}
                for k in xrange(league.matches_per_ai_pair):
                    while True:
                        indx = random.randrange(len(maps))
                        if not pickedMaps.has_key(indx) or len(maps) < league.matches_per_ai_pair:
                            map = maps[indx]
                            pickedMaps[indx] = True
                            break
                    matchRequest = MatchRequest(ai0, ai1, map, mod,\
                        league.speed, league.soft_timeout, league.hard_timeout,\
                        firstSide, secondSide, league.league_id)
                    matchRequests.append(matchRequest)
    #save all matches to the database
    Session.add_all(matchRequests)
    Session.commit()


# does for all leagues
def scheduleMatches():
    for league in Session.query(League):
        scheduleMatchesForLeague(league)
