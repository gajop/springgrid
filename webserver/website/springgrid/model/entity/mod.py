from base import *

class Mod(Base):
   __tablename__ = 'mods'

   mod_id = Column(Integer,primary_key=True)
   mod_name = Column(String(255), unique = True)
   mod_archivechecksum = Column(String(255))
   mod_url = Column(String(255))

   mod_sides = relationship("ModSide")

   def __init__(self, mod_name ):
      self.mod_name = mod_name
