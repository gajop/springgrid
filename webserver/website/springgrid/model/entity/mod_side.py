from base import *

class ModSide(Base):
   __tablename__ = 'mod_sides'

   mod_side_id = Column(Integer, primary_key=True)
   mod_side_name = Column(String(255), unique = False) #different mods can have the same side names
   mod_id = Column(Integer,ForeignKey('mods.mod_id'), nullable=False)

   def __init__(self, mod_side_name, mod_id):
      self.mod_side_name = mod_side_name
      self.mod_id = mod_id