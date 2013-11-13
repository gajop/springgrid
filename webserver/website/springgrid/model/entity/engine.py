from base import *


class Engine(Base):
    __tablename__ = 'engine'

    engine_id = Column(Integer, primary_key=True)
    engine_name = Column(String(255), unique=True)
    engine_archivechecksum = Column(String(255))
    engine_url = Column(String(255))

    def __init__(self, engine_name):
        self.engine_name = engine_name
