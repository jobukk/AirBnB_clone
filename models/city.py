#!/usr/bin/python3
""" class to  add city"""


from models.base_model import BaseModel


class City(BaseModel):
    """
    class inheriting BaseModel
    that has  state id and name of city
    """
    state_id = ""
    name = ""
