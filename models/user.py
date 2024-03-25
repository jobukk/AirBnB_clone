#!/usr/bin/python3
"""Defines the first user"""

from models.base_model import BaseModel

class User(BaseModel):
    """inherit from Basemodel"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
