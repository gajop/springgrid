from springgrid.tests import *

class TestSubmitrequestController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='submitrequest', action='index'))
        # Test response...
