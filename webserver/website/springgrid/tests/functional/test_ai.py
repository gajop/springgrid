from springgrid.tests import *

class TestAiController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='ai', action='index'))
        # Test response...
