# Copyright Hugh Perkins 2004, 2009
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

# functions for login, cookies etc...

from springgrid.lib.base import Session
from springgrid.model.meta import Account
from pylons import session

# returns True if password correct, otherwise false
def validateUsernamePassword(username, password):
    account = Session.query(Account).filter(Account.username == username ).first()
    if account == None:
        return False
    if account.passwordinfo == None:
        return False
    result = account.passwordinfo.checkPassword(password)
    return result

def logonUserWithAuthenticatedOpenID(openidurl):
    account = None
    # note: this could be optimized a little...
    for thisaccount in Session.query(Account):
        for openid in thisaccount.openids:
            if openid.openid == openidurl:
                account = thisaccount
    if account == None:
        # create new account
        account = Account(openidurl, openidurl)
        account.openids.append(OpenID(openidurl))
        Session.add(account)

    session['username'] = openidurl

def changePassword(username, password):
    account = Session.query(Account).filter(Account.username == username).first()
    account.passwordinfo.changePassword(password)
    Session.commit()
    return True

def logoutUser():
    pass
