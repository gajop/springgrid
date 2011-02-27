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
from meta import AI
import botrunnerhelper

def getallais():
    return Session.query(AI)

# return list of supported (ainame,aiversion) tuples
def getsupportedais( botrunnername ):
    botrunner = botrunnerhelper.getBotRunner(botrunnername)
    if botrunner == None:
        return []
    supportedais = []
    for ai in botrunner.supportedais:
        supportedais.append( [ ai.ai_name, ai.ai_version ] )

    return supportedais

def getAIs():
    return Session.query(AI).all()

def getAI( ainame, aiversion ):
    return Session.query(AI).filter(AI.ai_name == ainame ).filter(AI.ai_version == aiversion ).first()

def getAIOption( optionname ):
    return Session.query(AIOption).filter(AIOption.option_name == optionname ).first()

def addaiifdoesntexist(ainame, aiversion):
    ai = getAI( ainame, aiversion )
    if ai == None:
        try:
            ai = AI(ainame, aiversion )
            Session.add( ai )
            Session.commit()
        except:
            return(False,"error adding to db: " + str( sys.exc_value ) )

    return (True,'')

def setbotrunnersupportsthisai( botrunnername, ainame, aiversion ):
    botrunner = botrunnerhelper.getBotRunner( botrunnername )
    for ai in botrunner.supportedais:
        if ai.ai_name == ainame and ai.ai_version == aiversion:
            return (True,'')

    ai = getAI(ainame,aiversion)
    botrunner.supportedais.append(ai)
    Session.commit()
    return (True,'')

def setbotrunnernotsupportsthisai( botrunnername, ainame, aiversion ):
    botrunner = botrunnerhelper.getBotRunner( botrunnername )
    for ai in botrunner.supportedais:
        if ai.ai_name == ainame and ai.ai_version == aiversion:
            botrunner.supportedais.remove( ai )
    Session.commit()
    return (True,'')
