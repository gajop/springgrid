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
#

# handles storing and retrieving replays, or at least providing an appropriate path

import os

scriptdir = os.path.dirname(os.path.realpath( __file__ ))

# hacked in for now, we can refactor to different module name or something later
def getInfologPath(matchrequestid):
    if not os.path.isdir(scriptdir + "/../replays"):
        os.mkdir(scriptdir + "/../replays")
    # TODO: Serving raws
    #return scriptdir + "/../replays/infolog_" + str(matchrequestid) + ".tar.bz2"
    return scriptdir + "/../replays/infolog_" + str(matchrequestid) + ".txt"

def getInfologWebRelativePath(matchrequestid):
    # TODO: Serving raws
    #return "replays/infolog_" + str(matchrequestid) + ".tar.bz2"
    return "replays/infolog_" + str(matchrequestid) + ".txt"

def getReplayPath(matchrequestid):
    if not os.path.isdir(scriptdir + "/../replays"):
        os.mkdir(scriptdir + "/../replays")
    # TODO: Serving raws
    #return scriptdir + "/../replays/replay_" + str(matchrequestid) + ".tar.bz2"
    return scriptdir + "/../replays/replay_" + str(matchrequestid) + ".sdf"

def getReplayWebRelativePath(matchrequestid):
    # TODO: Serving raws
    #return "replays/replay_" + str(matchrequestid) + ".tar.bz2"
    return "replays/replay_" + str(matchrequestid) + ".sdf"
