"""The application's model objects"""
from springgrid.model.meta import Session, Base


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
 
    Session.configure(bind=engine)

__all__ = ['roles', 'botrunnerhelper','matchrequestcontroller',
   'replaycontroller', 'menu', 'maphelper', 'modhelper','aihelper',
   'loginhelper', 'sqlalchemysetup', 'tableclasses', 'accounthelper', 'leaguehelper', 'confighelper', 'jinjahelper' ]
