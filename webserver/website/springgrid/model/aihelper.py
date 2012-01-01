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

from springgrid.lib.base import Session
from meta import AI, AIBase
import botrunnerhelper
import sys

def getallais():
    return Session.query(AI)

# return list of supported (ainame,aiversion) tuples
def getsupportedais( botrunnername ):
    botrunner = botrunnerhelper.getBotRunner(botrunnername)
    if botrunner == None:
        return []
    supportedais = []
    for ai in botrunner.supportedais:
        supportedais.append([ai.ai_base.ai_base_name, ai.ai_version])

    return supportedais

def getAIs():
    return Session.query(AI).all()

def getAI(ainame, aiversion):
    ai_base = Session.query(AIBase).filter(AIBase.ai_base_name == ainame).first()
    if ai_base == None:
        return None
    else:
        return Session.query(AI).filter(AI.ai_base_id == ai_base.ai_base_id).filter(AI.ai_version == aiversion).first()

def getAIOption(optionname):
    return Session.query(AIOption).filter(AIOption.option_name == optionname).first()

def addaiifdoesntexist(ainame, aiversion):
    ai = getAI(ainame, aiversion)
    if ai == None:
        ai_base = Session.query(AIBase).filter(AIBase.ai_base_name == 
                                ainame).first()
        if ai_base == None:
            ai_base = AIBase(ainame)
            Session.add(ai_base)
            Session.flush()
        ai_base_id = ai_base.ai_base_id
        try:
            ai = AI(ai_base_id, aiversion)
            Session.add(ai)
            Session.commit()
        except:
            print sys.exc_value
            return(False, "error adding to db: " + str(sys.exc_value))

    return (True,'')

def setbotrunnersupportsthisai(botrunnername, ainame, aiversion):
    botrunner = botrunnerhelper.getBotRunner(botrunnername)
    for ai in botrunner.supportedais:
        if ai.ai_base.ai_base_name == ainame and ai.ai_version == aiversion:
            return (True,'')

    ai = getAI(ainame, aiversion)
    botrunner.supportedais.append(ai)
    Session.commit()
    return (True,'')

def setbotrunnernotsupportsthisai(botrunnername, ainame, aiversion):
    botrunner = botrunnerhelper.getBotRunner( botrunnername )
    for ai in botrunner.supportedais:
        if ai.ai_base.ai_base_name == ainame and ai.ai_version == aiversion:
            botrunner.supportedais.remove( ai )
    Session.commit()
    return (True,'')
