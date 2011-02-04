#!/usr/bin/python

from pylons import session

from jinja2 import Environment, PackageLoader

def getMenus():
    menus = []
    if 'user' in session:
        accountmenus = []
        accountmenus.append( ['Change Password...', 'changepasswordform.py'] )
        accountmenus.append( ['Logout', '/login/logout'] )
        menus.append([session['user'], accountmenus ])
    else:
        menus.append(["Login", [
                     [ 'Login ...', '/login/login' ]
                     ]])
    menus.append(['Results', [
      ['View match results', 'viewresults.py']
    ]])
    menus.append([ 'Runner', [
      ['View request queue', 'viewrequests.py'],
      ['Add request to queue...', 'submitrequestform.py'],
      ['Start botrunner instance...', 'startbotrunner.py']
    ]])

    menus.append([ 'Configuration', [
      ['Setup notes', 'setupnotes.py'],
      ['View available bot runners', 'viewbotrunners.py'],
      ['View available maps', 'viewmaps.py'],
      ['View available mods', 'viewmods.py'],
      ['View available ais', 'viewais.py'],
      ['View accounts', 'viewaccounts.py'],
      ['View global config', 'viewconfig.py' ],
      ['Run website diagnostics', 'diagnostics.py']
    ]])

    menus.append([ 'About', [
      ['About', 'about.py']
    ]])

    return menus

