from base import *

class MatchResult(Base):
   __tablename__ = 'matchresults'

   matchrequest_id = Column(Integer,ForeignKey('matchrequestqueue.matchrequest_id'),primary_key=True )
   matchresult = Column(String(255), nullable = False)

   def __init__(self, matchresult ):
      self.matchresult = matchresult