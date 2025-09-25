from sqlalchemy import Column, String, Integer, BigInteger, Boolean, DateTime, Text, JSON, Numeric, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import func
import enum
from typing import Optional
from datetime import datetime

from .base_model import BaseModel
from .enums import ApiType


class Api(BaseModel):
    __tablename__ = "apis"

    user_id = Column(BigInteger, nullable=False) # this should be a foreign key to users table
    type = Column(SQLEnum(ApiType), nullable=False)
    endpoint = Column(String(512), nullable=False)
    access_key = Column(String(512), nullable=False)
    secret_key = Column(String(512), nullable=True)
    load = Column(Integer, default=0, nullable=False)
    extra = Column(JSON, nullable=True)  # store extra config as JSON

