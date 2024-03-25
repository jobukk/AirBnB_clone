#!/usr/bin/python3
"""Defines the BaseModel class"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """Define the BaseModel class with common attributes"""
    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel.
        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key in ['created_at', 'updated_at']:
                        setattr(self, key, datetime.strptime(
                            value, "%Y-%m-%dT%H:%M:%S.%f"))
                    else:
                        setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
        if len(args) == 0 and len(kwargs) == 0:
            models.storage.new(self)

    def __str__(self):
        """Return the print/str representation of the BaseModel instance."""
        instance = self.__class__.__name__
        return f"[{instance}] ({self.id}) {self.__dict__}"

    def save(self):
        """Update updated_at with the current datetime."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Convert data to dictionary"""        
        dict = self.__dict__.copy()
        instance = self.__class__.__name__
        dict["__class__"] = instance
        dict["created_at"] = self.created_at.isoformat()
        dict["updated_at"] = self.updated_at.isoformat()
        return dict
