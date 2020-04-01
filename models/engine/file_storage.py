#!/usr/bin/python3
"""This is the file storage class for AirBnB"""
import json
import models


class FileStorage:
    """This class serializes instances to a JSON file and
    deserializes JSON file to instances
    Attributes:
        __file_path: path to the JSON file
        __objects: objects will be stored
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of __object
        """
        if cls:
            dict_obj_cls = {}
            for key, value in self.__objects.items():
                if cls.__name__ in key:
                    dict_obj_cls[key] = value
            return dict_obj_cls
        else:
            return self.__objects

    def new(self, obj):
        """sets __object to given obj
        Args:
            obj: given object
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            FileStorage.__objects[key] = obj

    def save(self):
        """serialize the file path to JSON file path
        """
        my_dict = {}
        for key, value in FileStorage.__objects.items():
            my_dict[key] = value.to_dict()
        with open(FileStorage.__file_path, mode='w', encoding="UTF-8") as fd:
            json.dump(my_dict, fd)

    def reload(self):
        '''
            Deserializes the JSON file to __objects.
        '''
        try:
            with open(FileStorage.__file_path, encoding="UTF8") as fd:
                FileStorage.__objects = json.load(fd)
                for key, val in FileStorage.__objects.items():
                    class_name = val["__class__"]
                    class_name = models.classes[class_name]
                    FileStorage.__objects[key] = class_name(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """delete obj
        """
        if obj is not None:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]

    def close(self):
        """
        call reload function for deserialization purposes
        """
        self.reload()
