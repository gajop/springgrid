from springgrid.tests import *

class TestLeagueController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='league', action='index'))
        # Test response...
