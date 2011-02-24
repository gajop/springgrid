from springgrid.tests import *

class TestModController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='mod', action='index'))
        # Test response...
