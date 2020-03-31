#!/usr/bin/python3
"""This is the file storage class for AirBnB"""
import json
from os import getenv
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """
    New engine for db
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Constructor
        """
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
            getenv("HBNB_MYSQL_USER"),
            getenv('HBNB_MYSQL_PWD'),
            getenv('HBNB_MYSQL_HOST'),
            getenv('HBNB_MYSQL_DB')),
            pool_pre_ping=True)

        environment_name = getenv("HBNB_MYSQL_ENV")
        if environment_name == "test":
            Base.metadata.drop_all(self.__engine)

        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

    def all(self, cls=None):
        """
        Return dictionary with selected class or
        return all classes if no class selected.
        """
        obj_dic = {}
        classes = [User, State, City, Place]
        if cls in classes:
            query = self.__session.query(eval(cls))
            for content in query:
                class_name = type(content).__name__
                object_id = content.id
                content_key = "{ }.{ }".format(class_name, object_id)
                obj_dic[content_key] = content
        else:
            for class_item in classes:
                query = self.__session.query(class_item)
                for item in query:
                    class_name = type(item).__name__
                    object_id = item.id
                    item_key = "{}.{}".format(class_name, object_id)
                    obj_dic[item_key] = item
        return obj_dic

    def new(self, obj):
        """
        Add the object to the current database session
        """
        if obj:
            try:
                self.__session.add(obj)
            except:
                pass

    def save(self):
        """
        Commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete from the current database session obj if not None
        """
        self.__session.delete(obj)

    def reload(self):
        """
        Bring it back
        """
        from models.base_model import Base
        Base.metadata.create_all(self.__engine)
        Session_n = sessionmaker(bind=self.__engine,
                                 expire_on_commit=False)
        Session = scoped_session(Session_n)
        self.__session = Session()

    def close(self):
        '''closes session'''
        self.__session.close()
