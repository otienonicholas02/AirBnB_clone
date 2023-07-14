#!/usr/bin/python3
"""Defines the City class."""

from models.base_model import BaseModel


class City(BaseModel):
    """Class that represents a city"""

    state_id = ""
    name = ""
