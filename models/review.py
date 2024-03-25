#!/usr/bin/python3
"""reviews class"""

from models.base_model import BaseModel


class Review(BaseModel):
    """
    class of BaseModel with
    place_id, user_id and text
    """

    place_id = ""
    user_id = ""
    text = ""
