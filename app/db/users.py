from app.db.utils import serialize_item, serialize_items
from app.db import DB

# User Collection Name
USER_COLLECTION = "users"

# User fields
USERNAME = "name"
EMAIL = "email"
PASSWORD_HASH = "password_hash"
PHONE = "phone"
ROLE = "role" #"member" "admin"


class UserResource:

    def __init__(self):
        self.collection = DB.get_collection(USER_COLLECTION)


    def create_user(self, username: str, email: str, password_hash: str, phone: str | None = None, role: str = "member"):
        user = {
            USERNAME: username,
            EMAIL: email,
            PASSWORD_HASH: password_hash,
            PHONE: phone,
            ROLE: role,
        }
        result = self.collection.insert_one(user)
        return str(result.inserted_id)

    def get_user_by_username(self, username: str):
        user = self.collection.find_one({USERNAME: username})
        return serialize_item(user)
        
    def get_user_by_email(self, email: str):
        user = self.collection.find_one({EMAIL: email})
        return serialize_item(user)
