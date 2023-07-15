#!/usr/bin/python3
"""Defines the User class."""

from models.base_model import BaseModel


class User(BaseModel):
    """Class that respresents it's uder and attributes."""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
