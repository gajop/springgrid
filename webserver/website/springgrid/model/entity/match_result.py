from base import *


class MatchResult(Base):
    __tablename__ = 'matchresult'

    matchrequest_id = Column(Integer,
            ForeignKey('matchrequest.matchrequest_id'),
            primary_key=True)
    matchresult = Column(String(255), nullable=False)

    def __init__(self, matchresult):
        self.matchresult = matchresult
