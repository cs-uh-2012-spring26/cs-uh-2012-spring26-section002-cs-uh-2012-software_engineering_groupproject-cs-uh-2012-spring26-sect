from app.db.utils import serialize_item, serialize_items
from app.db import DB

#Class collection name
CLASS_COLLECTION = "classes"
#Class fields
start_time = "start_time"
end_time = "end_time"
location = "location"
capacity = "capacity"
trainer_name = "trainer_name"
remaining_spots = "remaining_spots"

class ClassResource:
  def __init__(self):
    self.collection = DB.get_collection(CLASS_COLLECTION)
  def create_class(self, start_time_value: str, end_time_value:str, location_value: str, capacity_value:int, trainer_name_value: str):
    new_class = { #build a new class from imput given by trainer/admin
      start_time: start_time_value,
      end_time: end_time_value,
      location: location_value,
      capacity: capacity_value,
      trainer_name: trainer_name_value,
      remaining_spots: capacity_value
    }
    insert_result = self.collection.insert_one(new_class)
    new_class_id = insert_result.inserted_id
    return str(new_class_id)
