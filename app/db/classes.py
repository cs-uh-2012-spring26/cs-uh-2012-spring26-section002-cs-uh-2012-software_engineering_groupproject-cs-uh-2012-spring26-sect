from app.db.utils import serialize_item, serialize_items
from app.db import DB
from datetime import datetime, timedelta

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

  def get_upcoming_classes(self):
    #get all classes from database
    classes = self.collection.find({})
    classes_list = serialize_items(list(classes))

    now = datetime.now()
    latest_allowed = now+ timedelta(days=14) #show classes within next 2 weeks

    upcoming_classes =[]
    for one_class in classes_list:
      start_time_value = one_class.get(start_time) #read start time of each class
      #skip if start time is missing or invalid
      if not isinstance(start_time_value, str):
        continue
      try:
        class_start_datetime = datetime.fromisoformat(start_time_value)
      except Exception:
        continue #skip class if there is invalid date format
      #include only classes in upcoming 2 weeks
      if now<=class_start_datetime<=latest_allowed:
        upcoming_classes.append(one_class)
    return upcoming_classes
