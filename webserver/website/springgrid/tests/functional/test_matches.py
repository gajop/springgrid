from springgrid.tests import *

class TestMatchesController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='matches', action='index'))
        # Test response...
