from springgrid.tests import *

class TestBotrunnerController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='botrunner', action='index'))
        # Test response...
