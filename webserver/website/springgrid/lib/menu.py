#!/usr/bin/python

from pylons import session

from jinja2 import Environment, PackageLoader
import springgrid.lib.helpers as h

def getMenus():
    menus = []
    if 'user' in session:
        accountmenus = []
        accountmenus.append( ['Change Password...',
            h.url(controller='change_password', action='form')] )
        accountmenus.append( ['Logout',
            h.url(controller='login', action='logout')] )
        menus.append([session['user'], accountmenus ])
    else:
        menus.append(["Login", [
                     [ 'Login ...',
                         h.url(controller='login', action='form')]
                     ]])
    menus.append(['Results', [
      ['View match results',
          h.url(controller='matches', action='results')]
    ]])
    menus.append([ 'Runner', [
      ['View request queue',
          h.url(controller='matches', action='requests')],
      ['Add request to queue...',
          h.url(controller='submit_request', action='form')],
      ['Start botrunner instance...',
          h.url(controller='info', action='botrunner')]
    ]])

    menus.append([ 'Configuration', [
      ['Setup notes',
          h.url(controller='info', action='setupnotes')],
      ['View available bot runners',
          h.url(controller='botrunner', action='list')],
      ['View available maps',
          h.url(controller='map', action='list')],
      ['View available mods',
          h.url(controller='mod', action='list')],
      ['View available ais',
          h.url(controller='ai', action='list')],
      ['View accounts',
          h.url(controller='account', action='list')],
      ['View global config',
          h.url(controller='info', action='config') ],
      ['Run website diagnostics',
          h.url(controller='info', action='diagnostics')]
    ]])

    menus.append([ 'About', [
      ['About', h.url(controller='about', action='view')]
    ]])

    return menus
