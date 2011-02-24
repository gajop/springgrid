from springgrid.tests import *

class TestChangepasswordController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='changepassword', action='index'))
        # Test response...
