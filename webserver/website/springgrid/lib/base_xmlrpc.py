"""The base Controller API

Provides the BaseController class for subclassing.
"""
import traceback

from pylons.controllers import XMLRPCController

from springgrid.model.meta import Session

class BaseXMLRPCController(XMLRPCController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # XMLRPCController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return XMLRPCController.__call__(self, environ, start_response)
        except:
            traceback.print_exc()
        finally:
            Session.remove()
