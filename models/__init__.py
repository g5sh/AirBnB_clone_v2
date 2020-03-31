#!/usr/bin/python3
"""create a unique FileStorage instance for your application"""
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")

if storage_type == "db":
    storage = DBStorage()
    storage.reload()

else:
    classes = {"User": User,
               "BaseModel": BaseModel,
               "City": City,
               "Amenity": Amenity,
               "State": State,
               "Place": Place,
               "Review": Review}


    storage = FileStorage()
    storage.reload()
