import sys
import os
import datetime
import base64
import traceback

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from springgrid.lib.base_xmlrpc import BaseXMLRPCController, Session
from springgrid.model.meta import Map, Mod, ModSide, AI, MatchRequest, AIOption
from springgrid.model import botrunnerhelper, maphelper, modhelper, replaycontroller

from springgrid.model import *

class ApiWebserviceController(BaseXMLRPCController):
    # returns a list of mapnames
    def getmaps(self):
        return [i[0] for i in Session.query(Map.map_name)]

    # returns a list of modnames
    def getmods(self):
        return [i[0] for i in Session.query(Mod.mod_name)]

    # returns a dictionary of lists mapping from modname -> modname sides
    def getmodsides(self):
        return [{"mod_side_name" : i.mod_side_name, "mod_side_id" : i.mod_side_id, "mod_name" : Session.query(Mod.mod_name).filter(Mod.mod_id == i.mod_id).first()[0]} for i in Session.query(ModSide).all()]

    # returns [True, exists(map_name)] or [False, errormessage]
    def mapexists(self, map_name):
        map = maphelper.getMap(map_name)
        return [True, map != None ]

    # returns [True, exists(mod_name)] or [False, errormessage]
    def modexists(self, mod_name):
        mod = modhelper.getMod(mod_name)
        return [True, mod != None]

    # returns a list of {'ai_name': ainame, 'ai_version': aiversion } ] dictionaries
    def getais(self):
        ailist = []
        for ai in Session.query(AI):
            ailist.append({'ai_name': ai.ai_name, 'ai_version': ai.ai_version, 'ai_id':ai.ai_id})
        return ailist

    # schedule a single match
    # - 'ais' should contain a list of {'ai_name': ainame, 'ai_version': aiversion} dicts
    # containing all ais that should play on the map
    # - 'options' should contain a list of option name strings
    #
    # note: later versions of this function should be added with a new version number
    # ie v2, v3 etc... to avoid breaking the api for old clients
    # returns [True, matchrequest_id] or [False, errormessage ]
    def schedulematchv1(self, map_name, mod_name, ais, options, speed, 
            softtimeout, hardtimeout):
        map = Session.query(Map).filter(Map.map_name == map_name).first()
        mod = Session.query(Mod).filter(Mod.mod_name == mod_name).first()
        ai0 = Session.query(AI).filter(AI.ai_name == ais[0]['ai_name']).\
                filter(AI.ai_version == ais[0]['ai_version']).first()
        ai1 = Session.query(AI).filter(AI.ai_name == ais[1]['ai_name']).\
                filter(AI.ai_version == ais[1]['ai_version']).first()
        ai0Side = Session.query(ModSide).filter(ModSide.mod_side_name == \
                ais[0]['ai_side']).filter(ModSide.mod_id == mod.mod_id).first()
        ai1Side = Session.query(ModSide).filter(ModSide.mod_side_name == \
                ais[1]['ai_side']).filter(ModSide.mod_id == mod.mod_id).first()

        if map == None or mod == None or ai0 == None or ai1 == None:
            return [False, 'one of your parameters did not correspond to an existing map, mod or ai.  Please check and try again.']
        if softtimeout == None or hardtimeout == None:
            return [False, 'you need to specify both a hard timeout and a soft timeout for the match']
        if speed == None:
            speed = 1

        matchrequest = MatchRequest(ai0 = ai0, ai1 = ai1, map = map,
                mod = mod, speed = speed, softtimeout = softtimeout, 
                hardtimeout = hardtimeout, ai0_side = ai0Side, 
                ai1_side = ai1Side)
        Session.add(matchrequest)

        # add options:
        availableoptions = Session.query(AIOption)
        for option in availableoptions:
            if option.option_name in options:
                matchrequest.options.append(option)

        Session.commit()

        return [True, matchrequest.matchrequest_id]

    def schedulematchesv1(self,matches):
        matchrequest_ids = []
        for match in matches:
            map_name = match["map_name"]
            mod_name = match["mod_name"]
            options = match["options"]
            ais = match["ais"]
            softtimeout = match["softtimeout"]
            hardtimeout = match["hardtimeout"]
            speed = match["speed"]
            ai0_side = ais[0]['ai_side']
            ai1_side = ais[1]['ai_side']
            try:
                map = Session.query(Map).filter(Map.map_name == map_name ).first()
                mod = Session.query(Mod).filter(Mod.mod_name == mod_name ).first()
                ai0 = Session.query(AI).filter(AI.ai_name == ais[0]['ai_name']).filter(AI.ai_version == ais[0]['ai_version'] ).first()
                ai1 = Session.query(AI).filter(AI.ai_name == ais[1]['ai_name']).filter(AI.ai_version == ais[1]['ai_version'] ).first()
                ai0_side = Session.query(ModSide).filter(ModSide.mod_side_id == ai0_side).first()
                ai1_side = Session.query(ModSide).filter(ModSide.mod_side_id == ai1_side).first()

                if map == None or mod == None or ai0 == None or ai1 == None or ai0_side == None or ai1_side == None:
                    return [False,'one of your parameters did not correspond to an existing map, mod, ai or ai sides.  Please check and try again.']
                if softtimeout == None or hardtimeout == None:
                    return [False,'you need to specify both a hard timeout and a soft timeout for the match']
                if speed == None:
                    speed = 1

                matchrequest = MatchRequest( ai0 = ai0, ai1 = ai1, map = map, mod = mod, speed = speed, softtimeout = softtimeout, hardtimeout = hardtimeout, ai0_side = ai0_side, ai1_side = ai1_side )
                Session.add( matchrequest )

                # add options:
                availableoptions = Session.query(AIOption)
                for option in availableoptions:
                    if option.option_name in options:
                        matchrequest.options.append( option )

                matchrequest_ids.append(matchrequest.matchrequest_id)
            except:
                return (False,"An unexpected exception occurred: " + str( sys.exc_info() ) + "\n" + str( traceback.extract_tb( sys.exc_traceback ) ) )
        Session.commit()
        return [True, matchrequest_ids]

    # returns list of dictionaries
    # note: later versions of this function, with incompatiable changes, should be added with a new version number
    # ie v2, v3 etc... to avoid breaking the api for old clients
    # returns [True,list] if successful or [False,errormessage] if something went wrnog
    def getmatchrequestqueuev1(self):
        try:
            requests = Session.query(MatchRequest).filter(MatchRequest.matchresult == None )
            requeststoreturn = []
            for request in requests:
                options = []
                for option in request.options:
                    options.append(option.option_name)
                requeststoreturn.append( {
                   'matchrequest_id': request.matchrequest_id,
                   'map_name': request.map.map_name,
                   'mod_name': request.mod.mod_name,
                   'ais': [ { 'ai_name': request.ai0.ai_name, 'ai_version': request.ai0.ai_version },
                      { 'ai_name': request.ai1.ai_name, 'ai_version': request.ai1.ai_version } ],
                   'options': options,
                   'ai0_side': { 'mod_side_name' : request.ai0_side.mod_side_name, 'mod_side_id' : request.ai0_side.mod_side_id},
                   'ai1_side': { 'mod_side_name' : request.ai1_side.mod_side_name, 'mod_side_id' : request.ai1_side.mod_side_id}
                   } )
            return [True, requeststoreturn ]
        except:
            return (False,"An unexpected exception occurred: " + str( sys.exc_info() ) + "\n" + str( traceback.extract_tb( sys.exc_traceback ) ) )

    def getmatchesv1(self, matchrequest_ids):
        try:
            requests = Session.query(MatchRequest).filter(MatchRequest.matchrequest_id.in_(matchrequest_ids))
            resulttoreturn = []
            for request in requests:
                options = []
                for option in request.options:
                    options.append(option.option_name)
                newresulttoreturn = {
                   'matchrequest_id': request.matchrequest_id,
                   'map_name': request.map.map_name,
                   'mod_name': request.mod.mod_name,
                   'ais': [ { 'ai_name': request.ai0.ai_name, 'ai_version': request.ai0.ai_version },
                      { 'ai_name': request.ai1.ai_name, 'ai_version': request.ai1.ai_version } ],
                   'options': options,
                   'ai0_side': { 'mod_side_name' : request.ai0_side.mod_side_name, 'mod_side_id' : request.ai0_side.mod_side_id},
                   'ai1_side': { 'mod_side_name' : request.ai1_side.mod_side_name, 'mod_side_id' : request.ai1_side.mod_side_id},
                }
                if request.matchrequestinprogress != None and request.matchrequestinprogress.botrunner != None:
                    newresulttoreturn['botrunner_name'] = [True, request.matchrequestinprogress.botrunner.botrunner_name]
                else:
                    newresulttoreturn['botrunner_name'] = [False, '']
                if request.matchresult != None:
                    newresulttoreturn['matchresult'] = [True, request.matchresult.matchresult]
                else:
                    newresulttoreturn['matchresult'] = [False, '']
                if os.path.isfile(replaycontroller.getReplayPath(request.matchrequest_id) ):
                    newresulttoreturn['replayrelativeurl'] = replaycontroller.getReplayWebRelativePath(request.matchrequest_id)
                if os.path.isfile(replaycontroller.getInfologPath(request.matchrequest_id) ):
                    newresulttoreturn['infologrelativeurl'] = replaycontroller.getInfologWebRelativePath(request.matchrequest_id)
                resulttoreturn.append( newresulttoreturn )
            return [True, resulttoreturn]
        except:
            return (False,"An unexpected exception occurred: " + str( sys.exc_info() ) + "\n" + str( traceback.extract_tb( sys.exc_traceback ) ) )

    def getmatchv1(self, matchrequest_id):
        try:
            request = Session.query(MatchRequest).filter(MatchRequest.matchrequest_id == matchrequest_id).first()
            if request is not None:
                options = []
                for option in request.options:
                    options.append(option.option_name)
                newresulttoreturn = {
                   'matchrequest_id': request.matchrequest_id,
                   'map_name': request.map.map_name,
                   'mod_name': request.mod.mod_name,
                   'ais': [ { 'ai_name': request.ai0.ai_name, 'ai_version': request.ai0.ai_version },
                      { 'ai_name': request.ai1.ai_name, 'ai_version': request.ai1.ai_version } ],
                   'options': options,
                   'ai0_side': { 'mod_side_name' : request.ai0_side.mod_side_name, 'mod_side_id' : request.ai0_side.mod_side_id},
                   'ai1_side': { 'mod_side_name' : request.ai1_side.mod_side_name, 'mod_side_id' : request.ai1_side.mod_side_id}
                }
                if request.matchrequestinprogress.botrunner != None:
                    newresulttoreturn['botrunner_name'] = [True, request.matchrequestinprogress.botrunner.botrunner_name]
                else:
                    newresulttoreturn['botrunner_name'] = [False, '']
                if request.matchresult != None:
                    newresulttoreturn['matchresult'] = [True, request.matchresult.matchresult]
                else:
                    newresulttoreturn['matchresult'] = [False, '']
                if os.path.isfile(replaycontroller.getReplayPath(request.matchrequest_id) ):
                    newresulttoreturn['replayrelativeurl'] = replaycontroller.getReplayWebRelativePath(request.matchrequest_id)
                if os.path.isfile( replaycontroller.getInfologPath(request.matchrequest_id) ):
                    newresulttoreturn['infologrelativeurl'] = replaycontroller.getInfologWebRelativePath(request.matchrequest_id)
                return [True, newresulttoreturn]
            else:
                return [False, 'no match with such id']
        except:
            return (False,"An unexpected exception occurred: " + str( sys.exc_info() ) + "\n" + str( traceback.extract_tb( sys.exc_traceback ) ) )


    # returns list of dictionaries
    # note: later versions of this function, with incompatiable changes, should be added with a new version number
    # ie v2, v3 etc... to avoid breaking the api for old clients
    # returns [True,list] if successful or [False,errormessage] if something went wrnog
    def getmatchresultsv1(self):
        try:
            requests = Session.query(MatchRequest).filter(MatchRequest.matchresult != None )
            resultstoreturn = []
            for request in requests:
                options = []
                for option in request.options:
                    options.append(option.option_name)
                newresulttoreturn = {
                   'matchrequest_id': request.matchrequest_id,
                   'map_name': request.map.map_name,
                   'mod_name': request.mod.mod_name,
                   'ais': [ { 'ai_name': request.ai0.ai_name, 'ai_version': request.ai0.ai_version },
                      { 'ai_name': request.ai1.ai_name, 'ai_version': request.ai1.ai_version } ],
                   'options': options,
                   'botrunner_name': request.matchrequestinprogress.botrunner.botrunner_name,
                   'matchresult': request.matchresult.matchresult
                }
                if os.path.isfile( replaycontroller.getReplayPath(request.matchrequest_id) ):
                    newresulttoreturn['replayrelativeurl'] = replaycontroller.getReplayWebRelativePath(request.matchrequest_id)
                if os.path.isfile( replaycontroller.getInfologPath(request.matchrequest_id) ):
                    newresulttoreturn['infologrelativeurl'] = replaycontroller.getInfologWebRelativePath(request.matchrequest_id)
                resultstoreturn.append( newresulttoreturn )
            return [True, resultstoreturn ]
        except:
            return (False,"An unexpected exception occurred: " + str( sys.exc_info() ) + "\n" + str( traceback.extract_tb( sys.exc_traceback ) ) )
