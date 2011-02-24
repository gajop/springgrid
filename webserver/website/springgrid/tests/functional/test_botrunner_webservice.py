from springgrid.tests import *

class TestBotrunnerWebserviceController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='botrunner_webservice', action='index'))
        # Test response...
