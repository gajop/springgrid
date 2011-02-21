
class Map(Base):
   __tablename__ = 'maps'

   map_id = Column(Integer, primary_key = True)
   map_name = Column(String(255), unique = True)
   map_archivechecksum = Column(String(255))
   map_url = Column(String(255))

   def __init__(self, map_name):
      self.map_name = map_name
